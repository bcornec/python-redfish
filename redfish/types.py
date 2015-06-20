# coding=utf-8

import tortilla

# Global variable
TORTILLADEBUG = True

class Base(object):
    """Abstract class to manage types (Chassis, Servers etc...)."""
    
    def __init__(self,url,verify_cert, auth_token):
        global TORTILLADEBUG
        self.url=url
        self.verify_cert = verify_cert
        self.auth_token = auth_token
        
        self.apiUrl = tortilla.wrap(self.url, debug=TORTILLADEBUG)
        #self.apiUrl.headers.x-auth-token = self.auth_token
        self.data = self.apiUrl.get(verify=self.verify_cert, headers={'x-auth-token': self.auth_token})
        print self.data
    
class BaseCollection(Base):
    """Abstract class to manage types (Chassis, Servers etc...)."""
    
    def __init__(self, url, verify_cert, auth_token):
        super(BaseCollection, self).__init__(url, verify_cert, auth_token)
        
        self.links=[]
        
        #linksmembers = self.data.Links.Members
        linksmembers = self.data.links.Member
        for link in linksmembers:
            #self.links.append(getattr(link,"@odata.id"))
            self.links.append(getattr(link,"href"))
        print self.links


class Managers(Base):
    pass

class ManagersCollection(BaseCollection):
    pass   