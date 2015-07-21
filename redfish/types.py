# coding=utf-8

import sys
import pprint
from urlparse import urljoin
import requests
import tortilla
import config
import mapping

# Global variable


class Base(object):
    """Abstract class to manage types (Chassis, Servers etc...)."""

    def __init__(self, url, connection_parameters):
        global TORTILLADEBUG
        self.connection_parameters = connection_parameters # Uggly hack to check
        self.url = url
        self.api_url = tortilla.wrap(url, debug=config.TORTILLADEBUG)

        try:
            if connection_parameters.auth_token == None:
                self.data = self.api_url.get(verify=connection_parameters.verify_cert)
            else:
                self.data = self.api_url.get(verify=connection_parameters.verify_cert,
                                             headers={'x-auth-token': connection_parameters.auth_token}
                                             )
        except requests.ConnectionError as e:
            print e
            # Log and transmit the exception.
            config.logger.error("Connection error : %s", e)
            raise e
        print self.data

    def get_link_url(self, link_type):
        self.links=[]
        #links = self.data.links
        links = getattr(self.data, mapping.redfish_mapper.map_links())
        if link_type in links:
            return  urljoin(self.url, links[link_type][mapping.redfish_mapper.map_links_ref()])
        
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, url):
        self.__url = url


class BaseCollection(Base):
    """Abstract class to manage collection (Chassis, Servers etc...)."""

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
            self.links.append(urljoin(self.url, getattr(link, mapping.redfish_mapper.map_links_ref())))


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
    """Class to manage redfish SessionService data."""
    pass


class Managers(Base):
    pass


class ManagersCollection(BaseCollection):
    """Class to manage redfish ManagersCollection data."""
    def __init__(self, url, connection_parameters):
        super(ManagersCollection, self).__init__(url, connection_parameters)
        
        self.managers_list = []
        
        for link in self.links:
            self.managers_list.append(Managers(link, connection_parameters))
        


class Systems(Base):
    # TODO : Need to discuss with Bruno the required method.
    #        Also to check with the ironic driver requirement.
    def reset_system(self):
        # Craft the request
        action = dict()
        action['Action'] = 'Reset'
        action['ResetType'] = 'ForceRestart'

        # perform the POST action
        print self.api_url
        response = self.api_url.post(verify=self.connection_parameters.verify_cert,
                                     headers={'x-auth-token': self.connection_parameters.auth_token},
                                     data=action
                                        )
        #TODO : treat response.
        
    def get_bios_version(self):
        try:
            # Returned by proliant
            return self.data.Bios.Current.VersionString
        except:
            # Retuned by mockup.
            # Hopefully this kind of discrepencies will be fixed with Redfish 1.0 (August)
            return self.data.BiosVersion


class SystemsCollection(BaseCollection):
    """Class to manage redfish ManagersCollection data."""
    def __init__(self, url, connection_parameters):
        super(SystemsCollection, self).__init__(url, connection_parameters)
        
        self.systems_list = []
        
        for link in self.links:
            self.systems_list.append(Systems(link, connection_parameters))