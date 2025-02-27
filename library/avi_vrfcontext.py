#!/usr/bin/python3
#
# @author: Gaurav Rastogi (grastogi@avinetworks.com)
#          Eric Anderson (eanderson@avinetworks.com)
# module_check: supported
# Avi Version: 17.1.2
#
# Copyright: (c) 2017 Gaurav Rastogi, <grastogi@avinetworks.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: avi_vrfcontext
author: Gaurav Rastogi (@grastogi23) <grastogi@avinetworks.com>

short_description: Module for setup of VrfContext Avi RESTful Object
description:
    - This module is used to configure VrfContext object
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
    attrs:
        description:
            - Key/value vrfcontext attributes.
            - Field introduced in 20.1.2.
            - Allowed in basic edition, essentials edition, enterprise edition.
        type: list
    bfd_profile:
        description:
            - Bfd configuration profile.
            - Field introduced in 20.1.1.
            - Allowed in basic edition, essentials edition, enterprise edition.
        type: dict
    bgp_profile:
        description:
            - Bgp local and peer info.
        type: dict
    cloud_ref:
        description:
            - It is a reference to an object of type cloud.
        type: str
    debugvrfcontext:
        description:
            - Configure debug flags for vrf.
            - Field introduced in 17.1.1.
        type: dict
    description:
        description:
            - User defined description for the object.
        type: str
    gateway_mon:
        description:
            - Configure ping based heartbeat check for gateway in service engines of vrf.
            - Maximum of 32 items allowed.
        type: list
    internal_gateway_monitor:
        description:
            - Configure ping based heartbeat check for all default gateways in service engines of vrf.
            - Field introduced in 17.1.1.
        type: dict
    labels:
        description:
            - Key/value labels which can be used for object access policy permission scoping.
            - Field deprecated in 20.1.5.
            - Field introduced in 18.2.7, 20.1.1.
        type: list
    lldp_enable:
        description:
            - Enable lldp.
            - Field introduced in 18.2.10, 20.1.1.
            - Allowed in basic(allowed values- true) edition, essentials(allowed values- true) edition, enterprise edition.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
    markers:
        description:
            - List of labels to be used for granular rbac.
            - Field introduced in 20.1.5.
        type: list
    name:
        description:
            - Name of the object.
        required: true
        type: str
    static_routes:
        description:
            - List of staticroute.
        type: list
    system_default:
        description:
            - Boolean flag to set system_default.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        type: bool
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
- name: Example to create VrfContext object
  avi_vrfcontext:
    controller: 10.10.25.42
    username: admin
    password: something
    state: present
    name: sample_vrfcontext
"""

RETURN = '''
obj:
    description: VrfContext (api/vrfcontext) object
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
        attrs=dict(type='list',),
        bfd_profile=dict(type='dict',),
        bgp_profile=dict(type='dict',),
        cloud_ref=dict(type='str',),
        debugvrfcontext=dict(type='dict',),
        description=dict(type='str',),
        gateway_mon=dict(type='list',),
        internal_gateway_monitor=dict(type='dict',),
        labels=dict(type='list',),
        lldp_enable=dict(type='bool',),
        markers=dict(type='list',),
        name=dict(type='str', required=True),
        static_routes=dict(type='list',),
        system_default=dict(type='bool',),
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
    return avi_ansible_api(module, 'vrfcontext',
                           set())


if __name__ == '__main__':
    main()
