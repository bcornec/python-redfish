# coding=utf-8

import tortilla
import pprint



# Global variable
TORTILLADEBUG = True

class Base(object):
    """Abstract class to manage types (Chassis, Servers etc...)."""
    
    def __init__(self, url, connection_parameters):
        
        global TORTILLADEBUG
        self.api_url = tortilla.wrap(url, debug=TORTILLADEBUG)
        
        if connection_parameters.auth_token == None:
            self.data = self.api_url.get(verify=connection_parameters.verify_cert)
        else:
            self.data = self.api_url.get(verify=connection_parameters.verify_cert,
                                         headers={'x-auth-token': connection_parameters.auth_token}
                                        )
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


class Root(Base):
    """Class to manage redfish Root data."""
       
    
    def get_api_version(self):
        """Return api version.

        :returns:  string -- version
        :raises: AttributeError

        """
        try:
            version = self.data.RedfishVersion
        except AttributeError:
            version = self.data.ServiceVersion
        return(version)


class Managers(Base):
    pass

class ManagersCollection(BaseCollection):
    pass   