from threading import Thread
import time
from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails
from src.driver import CiscoIOSXRResourceDriver

tt = CiscoIOSXRResourceDriver()

context = ResourceCommandContext()
context.resource = ResourceContextDetails()
context.resource.name = 'dsada'
context.reservation = ReservationContextDetails()
# context.reservation.reservation_id = 'c3b410cb-70bd-4437-ae32-15ea17c33a74'
context.resource.attributes = dict()
context.resource.attributes['User'] = 'admin'
context.resource.attributes['SNMP Version'] = '2'
context.resource.attributes['SNMP Read Community'] = 'cisco'
# context.resource.attributes['SNMP Read Community'] = 'public'
context.resource.attributes['Password'] = 'admin'  # 'NuCpFxP8cJMCic8ePJokug=='
context.resource.attributes['Enable Password'] = 'cisco'
context.resource.attributes['Enable SNMP'] = 'False'
context.resource.attributes['Disable SNMP'] = 'False'
context.resource.attributes['CLI Connection Type'] = 'ssh'
context.resource.attributes['Sessions Concurrency Limit'] = '1'
context.resource.attributes['VRF Management Name'] = ''
context.resource.attributes['Backup Location'] = ''
context.resource.attributes['Sessions Concurrency Limit'] = '1'
context.resource.attributes['CLI TCP Port'] = '0'
context.resource.address = '192.168.1.120'
# context.resource.address = '192.168.73.72'
context.resource.name = '2950'
save_request = """
        {
            "custom_params": {
                "configuration_type" : "running",
                "vrf_management_name": ""
                }
        }"""
# restore_request = """{"saved_artifacts_info": {"saved_artifact": {"artifact_type": "ftp", "identifier": "//ftpuser:ftppass@192.168.85.24/folder1/2950-startup-291216-124035"}, "resource_name": "2950", "restore_rules": {"requires_same_resource": true}, "created_date": "2016-12-29T12:40:43.345000"}}"""
# restore_request = """{"saved_artifacts_info": {"saved_artifact": {"artifact_type": "ftp", "identifier": "//ftpuser:ftppass@192.168.85.24/folder1/2950-running-291216-124327"}, "resource_name": "2950", "restore_rules": {"requires_same_resource": true}, "created_date": "2016-12-29T12:43:39.006000"}}"""
restore_request = """{"saved_artifacts_info": {"saved_artifact": {"artifact_type": "flash", "identifier": "/2950-running-301216-142649"}, "resource_name": "2950", "restore_rules": {"requires_same_resource": true}, "created_date": "2016-12-30T14:27:03.416000"}}"""
restore_custom_params = """
        {
            "custom_params": {
                "restore_method" : "append"
                }
        }"""
request = """{
    "driverRequest" : {
        "actions" : [{
                "connectionId" : "457238ad-4023-49cf-8943-219cb038c0dc",
                "connectionParams" : {
                    "vlanId" : "450",
                    "mode" : "Access",
                    "vlanServiceAttributes" : [{
                            "attributeName" : "QnQ",
                            "attributeValue" : "False",
                            "type" : "vlanServiceAttribute"
                        }, {
                            "attributeName" : "CTag",
                            "attributeValue" : "",
                            "type" : "vlanServiceAttribute"
                        }, {
                            "attributeName" : "Isolation Level",
                            "attributeValue" : "Shared",
                            "type" : "vlanServiceAttribute"
                        }, {
                            "attributeName" : "Access Mode",
                            "attributeValue" : "Access",
                            "type" : "vlanServiceAttribute"
                        }, {
                            "attributeName" : "VLAN ID",
                            "attributeValue" : "45",
                            "type" : "vlanServiceAttribute"
                        }, {
                            "attributeName" : "Virtual Network",
                            "attributeValue" : "45",
                            "type" : "vlanServiceAttribute"
                        }, {
                            "attributeName" : "Pool Name",
                            "attributeValue" : "",
                            "type" : "vlanServiceAttribute"
                        }
                    ],
                    "type" : "setVlanParameter"
                },
                "connectorAttributes" : [],
                "actionId" : "457238ad-4023-49cf-8943-219cb038c0dc_4244579e-bf6f-4d14-84f9-32d9cacaf9d9",
                "actionTarget" : {
                    "fullName" : "2950/Chassis 0/FastEthernet0-23",
                    "fullAddress" : "192.168.42.235/0/23",
                    "type" : "actionTarget"
                },
                "customActionAttributes" : [],
                "type" : "setVlan"
            }
        ]
    }
}"""

tt.initialize(context)
# Thread(target=tt.orchestration_save, args=(context, None, save_request)).start()
# Thread(target=tt.orchestration_restore, args=(context, restore_request, restore_custom_params)).start()
# Thread(target=tt.health_check, args=(context,)).start()
# Thread(target=tt.ApplyConnectivityChanges, args=(context, request)).start()
Thread(target=tt.run_custom_command, args=(context, 'sh ver')).start()
Thread(target=tt.run_custom_config_command, args=(context, 'do sh run')).start()
# time.sleep(5)
# context.resource.attributes['User'] = 'root'
Thread(target=tt.get_inventory, args=(context, )).start()
# Thread(target=tt.save, args=(context, 'ftp://ftpuser:ftp@192.168.1.3', 'running', '')).start()
# Thread(target=tt.save, args=(context, 'tftp://192.168.30.110', '', '')).start()
# Thread(target=tt.restore, args=(context, 'ftp://ftpuser:ftp@192.168.1.3/2950-running-220217-213145', 'running',
#                                 'override', '')).start()
# Thread(target=tt.restore, args=(context, 'bootflash:/running', 'startup',
#                                 'append', '')).start()
# Thread(target=tt.send_custom_command, args=(context, 'show run')).start()
