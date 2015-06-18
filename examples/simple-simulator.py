import redfish

url = 'http://127.0.0.1:8000/redfish/v1'
user_name = 'Admin'
password = 'password'

''' Define a new log file '''
redfish.setLogFile("/var/log/python-redfish/python-refish-simulator.log")

''' remoteMgmt is a redfish.RedfishConnection object '''
remoteMgmt = redfish.connect(url, user_name, password, simulator=True)

print ("Redfish API version : %s \n" % remoteMgmt.getApiVersion()) 
print ("UUID : %s \n" % remoteMgmt.getApiUUID())

print remoteMgmt.getApiLinkToServer()

