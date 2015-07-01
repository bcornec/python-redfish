# coding=utf-8

""" Simple example to use python-redfish on HP Proliant servers """

import redfish

URL = 'http://10.3.222.104/rest/v1'
USER_NAME = 'demopaq'
PASSWORD = 'password'

''' remote_mgmt is a redfish.RedfishConnection object '''
remote_mgmt = redfish.connect(URL, USER_NAME, PASSWORD, verify_cert=False)

print ("Redfish API version : %s \n" % remote_mgmt.get_api_version())

remote_mgmt.logout()
