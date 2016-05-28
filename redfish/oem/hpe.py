# coding=utf-8
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import
from future import standard_library
from builtins import object

import pprint
import re
from ..types import Base, BaseCollection, Device
standard_library.install_aliases()

# Global variable


class NetworkAdaptersCollection(BaseCollection):
    '''Class to manage redfish hpe oem NetworkAdaptersCollection data.'''
    def __init__(self, url, connection_parameters):
        super(NetworkAdaptersCollection, self).__init__(url,
                                                        connection_parameters)
        self.network_adapters_dict = {}

        for link in self.links:
            index = re.search(r'NetworkAdapters/(\w+)', link)
            self.network_adapters_dict[index.group(1)] = NetworkAdapters(
                link, connection_parameters)


class NetworkAdapters(Base):
    '''Class to manage redfish hpe oem NetworkAdapters data.'''

    def get_mac(self):
        '''Get NetworkAdapters mac address

        :returns:  mac adresses or "Not available"
        :rtype: list

        '''

        macaddresses = []

        try:
            for port in self.data.PhysicalPorts:
                mac = port['MacAddress']
                macaddresses.append(mac)

            return macaddresses
        except AttributeError:
            return "Not available"

    def get_structured_name(self):
        '''Get NetworkAdapters StructuredName

        :returns: StructuredName or "Not available"
        :rtype: string

        '''
        try:
            return self.data.StructuredName
        except AttributeError:
            return "Not available"

    def get_uefi_path(self):
        '''Get networkadapters uefi path

        :returns: UEFIDevicePath or "Not available"
        :rtype: string

        '''
        try:
            return self.data.UEFIDevicePath
        except AttributeError:
            return "Not available"
