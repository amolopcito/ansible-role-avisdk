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
module: avi_gslb
author: Gaurav Rastogi (@grastogi23) <grastogi@avinetworks.com>

short_description: Module for setup of Gslb Avi RESTful Object
description:
    - This module is used to configure Gslb object
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
    async_interval:
        description:
            - Frequency with which messages are propagated to vs mgr.
            - Value of 0 disables async behavior and rpc are sent inline.
            - Allowed values are 0-5.
            - Field introduced in 18.2.3.
            - Unit is sec.
            - Default value when not specified in API or module is interpreted by Avi Controller as 0.
        version_added: "2.9"
        type: int
    clear_on_max_retries:
        description:
            - Max retries after which the remote site is treated as a fresh start.
            - In fresh start all the configs are downloaded.
            - Allowed values are 1-1024.
            - Default value when not specified in API or module is interpreted by Avi Controller as 20.
        type: int
    client_ip_addr_group:
        description:
            - Group to specify if the client ip addresses are public or private.
            - Field introduced in 17.1.2.
        version_added: "2.4"
        type: dict
    description:
        description:
            - User defined description for the object.
        type: str
    dns_configs:
        description:
            - Sub domain configuration for the gslb.
            - Gslb service's fqdn must be a match one of these subdomains.
        type: list
    enable_config_by_members:
        description:
            - Allows enable/disable of gslbservice pool groups and pool members from the gslb follower members.
            - Field introduced in 20.1.5.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        type: bool
    error_resync_interval:
        description:
            - Frequency with which errored messages are resynced to follower sites.
            - Value of 0 disables resync behavior.
            - Allowed values are 60-3600.
            - Special values are 0 - 'disable'.
            - Field introduced in 18.2.3.
            - Unit is sec.
            - Default value when not specified in API or module is interpreted by Avi Controller as 300.
        version_added: "2.9"
        type: int
    is_federated:
        description:
            - This field indicates that this object is replicated across gslb federation.
            - Field introduced in 17.1.3.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        version_added: "2.4"
        type: bool
    leader_cluster_uuid:
        description:
            - Mark this site as leader of gslb configuration.
            - This site is the one among the avi sites.
        required: true
        type: str
    maintenance_mode:
        description:
            - This field disables the configuration operations on the leader for all federated objects.
            - Cud operations on gslb, gslbservice, gslbgeodbprofile and other federated objects will be rejected.
            - The rest-api disabling helps in upgrade scenarios where we don't want configuration sync operations to the gslb member when the member is being
            - upgraded.
            - This configuration programmatically blocks the leader from accepting new gslb configuration when member sites are undergoing upgrade.
            - Field introduced in 17.2.1.
            - Default value when not specified in API or module is interpreted by Avi Controller as False.
        version_added: "2.5"
        type: bool
    name:
        description:
            - Name for the gslb object.
        required: true
        type: str
    replication_policy:
        description:
            - Policy for replicating configuration to the active follower sites.
            - Field introduced in 20.1.1.
        type: dict
    send_interval:
        description:
            - Frequency with which group members communicate.
            - Allowed values are 1-3600.
            - Unit is sec.
            - Default value when not specified in API or module is interpreted by Avi Controller as 15.
        type: int
    send_interval_prior_to_maintenance_mode:
        description:
            - The user can specify a send-interval while entering maintenance mode.
            - The validity of this 'maintenance send-interval' is only during maintenance mode.
            - When the user leaves maintenance mode, the original send-interval is reinstated.
            - This internal variable is used to store the original send-interval.
            - Field introduced in 18.2.3.
            - Unit is sec.
        version_added: "2.9"
        type: int
    sites:
        description:
            - Select avi site member belonging to this gslb.
            - Minimum of 1 items required.
        required: true
        type: list
    tenant_ref:
        description:
            - It is a reference to an object of type tenant.
        type: str
    tenant_scoped:
        description:
            - This field indicates tenant visibility for gs pool member selection across the gslb federated objects.
            - Field introduced in 20.1.4.
            - Default value when not specified in API or module is interpreted by Avi Controller as True.
        type: bool
    third_party_sites:
        description:
            - Third party site member belonging to this gslb.
            - Field introduced in 17.1.1.
        type: list
    url:
        description:
            - Avi controller URL of the object.
        type: str
    uuid:
        description:
            - Uuid of the gslb object.
        type: str
    view_id:
        description:
            - The view-id is used in change-leader mode to differentiate partitioned groups while they have the same gslb namespace.
            - Each partitioned group will be able to operate independently by using the view-id.
            - Default value when not specified in API or module is interpreted by Avi Controller as 0.
        type: int


extends_documentation_fragment:
    - avi
'''

EXAMPLES = """
- name: Example to create Gslb object
  avi_gslb:
    name: "test-gslb"
    avi_credentials:
      username: '{{ username }}'
      password: '{{ password }}'
      controller: '{{ controller }}'
    sites:
      - name: "test-site1"
        username: "gslb_username"
        password: "gslb_password"
        ip_addresses:
          - type: "V4"
            addr: "10.10.28.83"
        enabled: True
        member_type: "GSLB_ACTIVE_MEMBER"
        port: 443
        cluster_uuid: "cluster-d4ee5fcc-3e0a-4d4f-9ae6-4182bc605829"
      - name: "test-site2"
        username: "gslb_username"
        password: "gslb_password"
        ip_addresses:
          - type: "V4"
            addr: "10.10.28.86"
        enabled: True
        member_type: "GSLB_ACTIVE_MEMBER"
        port: 443
        cluster_uuid: "cluster-0c37ae8d-ab62-410c-ad3e-06fa831950b1"
    dns_configs:
      - domain_name: "test1.com"
      - domain_name: "test2.com"
    leader_cluster_uuid: "cluster-d4ee5fcc-3e0a-4d4f-9ae6-4182bc605829"

- name: Update Gslb site's configurations (Patch Add Operation)
  avi_gslb:
    avi_credentials:
      username: '{{ username }}'
      password: '{{ password }}'
      controller: '{{ controller }}'
    avi_api_update_method: patch
    avi_api_patch_op: add
    leader_cluster_uuid: "cluster-d4ee5fcc-3e0a-4d4f-9ae6-4182bc605829"
    name: "test-gslb"
    dns_configs:
      - domain_name: "temp1.com"
      - domain_name: "temp2.com"
    sites:
      - name: "test-site1"
        username: "gslb_username"
        password: "gslb_password"
        ip_addresses:
          - type: "V4"
            addr: "10.10.21.13"
        enabled: True
        member_type: "GSLB_ACTIVE_MEMBER"
        port: 283
        cluster_uuid: "cluster-d4ee5fcc-3e0a-4d4f-9ae6-4182bc605829"

- name: Update Gslb site's configurations (Patch Replace Operation)
  avi_gslb:
    avi_credentials:
      username: "{{ username }}"
      password: "{{ password }}"
      controller: "{{ controller }}"
    # On basis of cluster leader uuid dns_configs is set for that perticular leader cluster
    leader_cluster_uuid: "cluster-84aa795f-8f09-42bb-97a4-5103f4a53da9"
    name: "test-gslb"
    avi_api_update_method: patch
    avi_api_patch_op: replace
    dns_configs:
      - domain_name: "test3.com"
      - domain_name: "temp3.com"
    sites:
      - name: "test-site1"
        username: "gslb_username"
        password: "gslb_password"
        ip_addresses:
          - type: "V4"
            addr: "10.10.11.24"
        enabled: True
        member_type: "GSLB_ACTIVE_MEMBER"
        port: 283
        cluster_uuid: "cluster-d4ee5fcc-3e0a-4d4f-9ae6-4182bc605829"

- name: Delete Gslb site's den_vses configurations (Patch Delete(dns_vses) Operation)
  avi_gslb:
    avi_credentials:
      username: "{{ username }}"
      password: "{{ password }}"
      controller: "{{ controller }}"
    # On basis of cluster leader uuid dns_configs is set for that perticular leader cluster
    leader_cluster_uuid: "cluster-84aa795f-8f09-42bb-97a4-5103f4a53da9"
    name: "test-gslb"
    avi_api_update_method: patch
    avi_api_patch_op: delete
    dns_configs:
    sites:
      - ip_addresses: "10.10.28.83"
      - ip_addresses: "10.10.28.86"

- name: Delete Gslb complete site's configurations (Patch Delete(site) Operation)
  avi_gslb:
    avi_credentials: "{{ avi_credentials }}"
    api_version: 18.2.8
    avi_api_update_method: patch
    avi_api_patch_op: delete
    patch_level: '/site'
    name: gslb.lab2.local
    leader_cluster_uuid: "cluster-84aa795f-8f09-42bb-97a4-5103f4a53da9"
    dns_configs:
    sites:
      - ip_addresses: 10.10.28.83
"""

RETURN = '''
obj:
    description: Gslb (api/gslb) object
    returned: success, changed
    type: dict
'''

from ansible.module_utils.basic import AnsibleModule
try:
    from avi.sdk.utils.ansible_utils import avi_common_argument_spec
    from avi.sdk.avi_api import ApiSession, AviCredentials
    from avi.sdk.utils.ansible_utils import (
        avi_ansible_api, avi_common_argument_spec)
    HAS_AVI = True
except ImportError:
    HAS_AVI = False

def patch_add_gslb(module, gslb_obj):
    sites = module.params['sites']
    dns_configs = module.params.get("dns_configs", None)
    if 'dns_configs' in gslb_obj:
        gslb_obj['dns_configs'].extend(dns_configs)
        gslb_obj['dns_configs'] = list({v['domain_name'] : v for v in
                                        gslb_obj['dns_configs']}.values())
    else:
        gslb_obj['dns_configs'] = dns_configs
    if sites:
        for site in sites:
            site_ips = site.get('ip_addresses', None)
            if not site_ips:
                return module.fail_json(msg=(
                        "ip_addr of site %s in a configuration is mandatory. "
                        "Please provide ip_addresses i.e. gslb site's ip." %
                        module.params['name']))
            current_gslb_sites = gslb_obj.get('sites', [])
            for current_gslb_site in current_gslb_sites:
                if current_gslb_site['name'] == site['name']:
                    for key, val in site.items():
                        if (key == 'dns_vses' and 'dns_vses' in
                                current_gslb_site):
                            current_gslb_site['dns_vses'].extend(val)
                            current_gslb_site['dns_vses'] = list(
                                {v['dns_vs_uuid']: v for v in
                                 current_gslb_site['dns_vses']}.values())
                        else:
                            current_gslb_site[key] = val
                    break
            else:
                gslb_obj['sites'].append(site)
    return gslb_obj


def patch_replace_gslb(module, gslb_obj):
    sites = module.params['sites']
    dns_configs = module.params.get("dns_configs", None)
    if dns_configs:
        gslb_obj['dns_configs'] = dns_configs
    if sites:
        for site in sites:
            site_ips = site.get('ip_addresses', None)
            if not site_ips:
                return module.fail_json(msg=(
                        "ip_addr of site %s in a configuration is mandatory. "
                        "Please provide ip_addresses i.e. gslb site's ip." %
                        module.params['name']))
            current_gslb_sites = gslb_obj.get('sites', [])
            for current_gslb_site in current_gslb_sites:
                if current_gslb_site['name'] == site['name']:
                    for key, val in site.items():
                        current_gslb_site[key] = val
    return gslb_obj


def patch_delete_gslb(module, gslb_obj):
    sites = module.params['sites']
    gslb_obj['dns_configs'] = []
    if sites:
        for site in sites:
            site_ips = site.get('ip_addresses', None)
            if not site_ips:
                return module.fail_json(msg=(
                        "ip_addr of site %s in a configuration is mandatory. "
                        "Please provide ip_addresses i.e. gslb site's ip." %
                        module.params['name']))
            current_gslb_sites = gslb_obj.get('sites', [])
            for current_gslb_site in current_gslb_sites:
                if site_ips == current_gslb_site['ip_addresses'][0]['addr']:
                    if module.params['patch_level'] == '/site':
                        gslb_obj['sites'].remove(current_gslb_site)
                    else:
                        current_gslb_site['dns_vses'] = []
    return gslb_obj


def main():
    argument_specs = dict(
        state=dict(default='present',
                   choices=['absent', 'present']),
        avi_api_update_method=dict(default='put',
                                   choices=['put', 'patch']),
        avi_api_patch_op=dict(choices=['add', 'replace', 'delete']),
        patch_level=dict(type='str', default='/site/dns_vses',
                         choices=['/site/dns_vses', '/site']),
        async_interval=dict(type='int',),
        clear_on_max_retries=dict(type='int',),
        client_ip_addr_group=dict(type='dict',),
        description=dict(type='str',),
        dns_configs=dict(type='list',),
        enable_config_by_members=dict(type='bool',),
        error_resync_interval=dict(type='int',),
        is_federated=dict(type='bool',),
        leader_cluster_uuid=dict(type='str', required=True),
        maintenance_mode=dict(type='bool',),
        name=dict(type='str', required=True),
        replication_policy=dict(type='dict',),
        send_interval=dict(type='int',),
        send_interval_prior_to_maintenance_mode=dict(type='int',),
        sites=dict(type='list', required=True),
        tenant_ref=dict(type='str',),
        tenant_scoped=dict(type='bool',),
        third_party_sites=dict(type='list',),
        url=dict(type='str',),
        uuid=dict(type='str',),
        view_id=dict(type='int',),
    )
    argument_specs.update(avi_common_argument_spec())
    module = AnsibleModule(
        argument_spec=argument_specs, supports_check_mode=True)
    if not HAS_AVI:
        return module.fail_json(msg=(
            'Avi python API SDK (avisdk>=17.1) or requests is not installed. '
            'For more details visit https://github.com/avinetworks/sdk.'))
    api_method = module.params['avi_api_update_method']
    if str(api_method).lower() == 'patch':
        patch_op = module.params['avi_api_patch_op']
        # Create controller session
        api_creds = AviCredentials()
        api_creds.update_from_ansible_module(module)
        api = ApiSession.get_session(
            api_creds.controller, api_creds.username,
            password=api_creds.password, timeout=api_creds.timeout,
            tenant=api_creds.tenant, tenant_uuid=api_creds.tenant_uuid,
            token=api_creds.token, port=api_creds.port)
        # Get existing gslb objects
        rsp = api.get('gslb', api_version=api_creds.api_version)
        existing_gslb = rsp.json()
        gslb = existing_gslb['results']
        for gslb_obj in gslb:
            if (gslb_obj['leader_cluster_uuid'] ==
                    module.params['leader_cluster_uuid']):
                if str(patch_op).lower() == 'add':
                    patch_add_gslb(module, gslb_obj)
                elif str(patch_op).lower() == 'replace':
                    patch_replace_gslb(module, gslb_obj)
                elif str(patch_op).lower() == 'delete':
                    patch_delete_gslb(module, gslb_obj)
            module.params.update(gslb_obj)
            module.params.pop("patch_level")
            module.params.update(
                {
                    'avi_api_update_method': 'put',
                    'state': 'present'
                }
            )

    return avi_ansible_api(module, 'gslb',
                           set())


if __name__ == '__main__':
    main()
