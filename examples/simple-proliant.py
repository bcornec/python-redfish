import redfish

url = 'http://10.3.222.104/rest/v1'
user_name = 'demopaq'
password = 'password'

''' remoteMgmt is a redfish.RedfishConnection object '''
remoteMgmt = redfish.connect(url, user_name, password, verifyCert=False)

print ("Redfish API version : %s \n" % remoteMgmt.getApiVersion()) 

remoteMgmt.logout()

