#!/usr/bin/python3
#
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
# Avi Version: 17.1.1
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: avi_httppolicyset
author: Gaurav Rastogi (@grastogi23) <grastogi@avinetworks.com>

short_description: Module for setup of HTTPPolicySet Avi RESTful Object
description:
    - This module is used to configure HTTPPolicySet object
    - more examples at U(https://github.com/avinetworks/devops)
requirements: [ avisdk ]
version_added: "2.4"
options:
    state:
        description:
            - The state that should be applied on the entity.
        default: present
        choices: ["absent", "present"]
        type: str
    avi_api_update_method:
        description:
            - Default method for object update is HTTP PUT.
            - Setting to patch will override that behavior to use HTTP PATCH.
        version_added: "2.5"
        default: put
        choices: ["put", "patch"]
        type: str
    avi_api_patch_op:
        description:
            - Patch operation to use when using avi_api_update_method as patch.
        version_added: "2.5"
        choices: ["add", "replace", "delete"]
        type: str
    cloud_config_cksum:
        description:
            - Checksum of cloud configuration for pool.
            - Internally set by cloud connector.
        type: str
    created_by:
        description:
            - Creator name.
        type: str
    description:
        description:
            - User defined description for the object.
        type: str
    http_request_policy:
        description:
            - Http request policy for the virtual service.
        type: dict
    http_response_policy:
        description:
            - Http response policy for the virtual service.
        type: dict
    http_security_policy:
        description:
            - Http security policy for the virtual service.
        type: dict
    ip_reputation_db_ref:
        description:
            - Ip reputation database.
            - It is a reference to an object of type ipreputationdb.
            - Field introduced in 20.1.3.
        type: str
    is_internal_policy:
        description:
            - Boolean flag to set is_internal_policy.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        type: bool
    labels:
        description:
            - Key value pairs for granular object access control.
            - Also allows for classification and tagging of similar objects.
            - Field deprecated in 20.1.5.
            - Field introduced in 20.1.2.
            - Maximum of 4 items allowed.
        type: list
    markers:
        description:
            - List of labels to be used for granular rbac.
            - Field introduced in 20.1.5.
        type: list
    name:
        description:
            - Name of the http policy set.
        required: true
        type: str
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
        type: str
    url:
        description:
            - Avi controller URL of the object.
        type: str
    uuid:
        description:
            - Uuid of the http policy set.
        type: str


extends_documentation_fragment:
    - avi
'''

EXAMPLES = """
- name: Create a HTTP Policy set two switch between testpool1 and testpool2
  avi_httppolicyset:
    controller: 10.10.27.90
    username: admin
    password: AviNetworks123!
    name: test-HTTP-Policy-Set
    tenant_ref: /api/tenant?name=admin
    http_request_policy:
    rules:
      - index: 1
        enable: true
        name: test-test1
        match:
          path:
            match_case: INSENSITIVE
            match_str:
              - /test1
            match_criteria: EQUALS
        switching_action:
          action: HTTP_SWITCHING_SELECT_POOL
          status_code: HTTP_LOCAL_RESPONSE_STATUS_CODE_200
          pool_ref: "/api/pool?name=testpool1"
      - index: 2
        enable: true
        name: test-test2
        match:
          path:
            match_case: INSENSITIVE
            match_str:
              - /test2
            match_criteria: CONTAINS
        switching_action:
          action: HTTP_SWITCHING_SELECT_POOL
          status_code: HTTP_LOCAL_RESPONSE_STATUS_CODE_200
          pool_ref: "/api/pool?name=testpool2"
    is_internal_policy: false
"""

RETURN = '''
obj:
    description: HTTPPolicySet (api/httppolicyset) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from avi.sdk.utils.ansible_utils import avi_common_argument_spec
    from avi.sdk.utils.ansible_utils import (
        avi_ansible_api, avi_common_argument_spec)
    HAS_AVI = True
except ImportError:
    HAS_AVI = False


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        cloud_config_cksum=dict(type='str',),
        created_by=dict(type='str',),
        description=dict(type='str',),
        http_request_policy=dict(type='dict',),
        http_response_policy=dict(type='dict',),
        http_security_policy=dict(type='dict',),
        ip_reputation_db_ref=dict(type='str',),
        is_internal_policy=dict(type='bool',),
        labels=dict(type='list',),
        markers=dict(type='list',),
        name=dict(type='str', required=True),
        tenant_ref=dict(type='str',),
        url=dict(type='str',),
        uuid=dict(type='str',),
    )
    argument_specs.update(avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/avinetworks/sdk.'))
    return avi_ansible_api(module, 'httppolicyset',
                           set())


if __name__ == '__main__':
    main()
