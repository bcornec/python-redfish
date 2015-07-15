# coding=utf-8

""" Simple example to use python-redfish with DMTF simulator """

import redfish

URL = 'http://127.0.0.1:8000/redfish/v1'
USER_NAME = 'Admin'
PASSWORD = 'password'

''' Define a new log file '''
redfish.set_log_file("/var/log/python-redfish/python-redfish-simulator.log")

''' remoteMgmt is a redfish.RedfishConnection object '''
remoteMgmt = redfish.connect(URL, USER_NAME, PASSWORD,
                             simulator=True, enforceSSL=False)

print ("Redfish API version : %s \n" % remoteMgmt.get_api_version())
print ("UUID : %s \n" % remoteMgmt.Root.get_api_UUID())

#print remoteMgmt.get_api_link_to_server()
