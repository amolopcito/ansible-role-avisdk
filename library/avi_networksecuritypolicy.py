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
module: avi_networksecuritypolicy
author: Gaurav Rastogi (@grastogi23) <grastogi@avinetworks.com>

short_description: Module for setup of NetworkSecurityPolicy Avi RESTful Object
description:
    - This module is used to configure NetworkSecurityPolicy object
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
            - Checksum of cloud configuration for network sec policy.
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
    ip_reputation_db_ref:
        description:
            - Ip reputation database.
            - It is a reference to an object of type ipreputationdb.
            - Field introduced in 20.1.1.
            - Allowed in basic edition, essentials edition, enterprise edition.
        type: str
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
            - Name of the object.
        type: str
    rules:
        description:
            - List of networksecurityrule.
        type: list
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
            - Unique object identifier of the object.
        type: str


extends_documentation_fragment:
    - avi
'''

EXAMPLES = """
  - name: Create a network security policy to block clients represented by ip group known_attackers
    avi_networksecuritypolicy:
      controller: '{{ controller }}'
      username: '{{ username }}'
      password: '{{ password }}'
      name: vs-gurutest-ns
      rules:
      - action: NETWORK_SECURITY_POLICY_ACTION_TYPE_DENY
        age: 0
        enable: true
        index: 1
        log: false
        match:
          client_ip:
            group_refs:
            - Demo:known_attackers
            match_criteria: IS_IN
        name: Rule 1
      tenant_ref: /api/tenant?name=Demo
"""

RETURN = '''
obj:
    description: NetworkSecurityPolicy (api/networksecuritypolicy) object
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
        ip_reputation_db_ref=dict(type='str',),
        labels=dict(type='list',),
        markers=dict(type='list',),
        name=dict(type='str',),
        rules=dict(type='list',),
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
    return avi_ansible_api(module, 'networksecuritypolicy',
                           set())


if __name__ == '__main__':
    main()
