# coding=utf-8

import pprint
from urlparse import urljoin
import tortilla
import mapping

# Global variable
TORTILLADEBUG = True

class Base(object):
    """Abstract class to manage types (Chassis, Servers etc...)."""

    def __init__(self, url, connection_parameters):
        global TORTILLADEBUG
        self.__url = url
        self.api_url = tortilla.wrap(url, debug=TORTILLADEBUG)

        if connection_parameters.auth_token == None:
            self.data = self.api_url.get(verify=connection_parameters.verify_cert)
        else:
            self.data = self.api_url.get(verify=connection_parameters.verify_cert,
                                         headers={'x-auth-token': connection_parameters.auth_token}
                                        )
        print self.data

    def get_link_url(self, link_type):
        self.links=[]
        #links = self.data.links
        links = getattr(self.data, mapping.redfish_mapper.map_links())
        if link_type in links:
            return  urljoin(self.__url, links[link_type][mapping.redfish_mapper.map_links_ref()])


class BaseCollection(Base):
    """Abstract class to manage types (Chassis, Servers etc...)."""

    def __init__(self, url, connection_parameters):
        super(BaseCollection, self).__init__(url, connection_parameters)

        self.links=[]

        #linksmembers = self.data.Links.Members
        #linksmembers = self.data.links.Member
        linksmembers = getattr(self.data, mapping.redfish_mapper.map_links())
        linksmembers = getattr(linksmembers, mapping.redfish_mapper.map_members())
        for link in linksmembers:
            #self.links.append(getattr(link,"@odata.id"))
            #self.links.append(getattr(link,"href"))
            self.links.append(getattr(link, mapping.redfish_mapper.map_links_ref()))
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

    def get_api_UUID(self):
        return self.data.UUID


    def get_api_link_to_server(self):
        """Return api link to server.

        :returns:  string -- path

        """
        return getattr(self.root.Links.Systems, "@odata.id")



class SessionService(Base):
    pass

class Managers(Base):
    pass

class ManagersCollection(BaseCollection):
    pass