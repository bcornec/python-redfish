import redfish

host = '127.0.0.1:8000'
user_name = 'Admin'
password = 'password'

''' remoteMgmt is a redfish.RedfishConnection object '''
remoteMgmt = redfish.connect(host, user_name, password)

print remoteMgmt.getApiVersion()