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
    '''Class to manage redfish NetworkAdaptersCollection data.'''
    def __init__(self, url, connection_parameters):
        super(NetworkAdaptersCollection, self).__init__(url, connection_parameters)

        self.chassis_dict = {}

        for link in self.links:
            index = re.search(r'NetworkAdapters/(\w+)', link)
            self.chassis_dict[index.group(1)] = NetworkAdapters(
                link, connection_parameters)


class NetworkAdapters(Device):
    '''Class to manage redfish NetworkAdapters data.'''
    def __init__(self, url, connection_parameters):
        '''Class constructor'''
        super(NetworkAdapters, self).__init__(url, connection_parameters)

        try:
            self.thermal = Thermal(self.get_link_url('Thermal'),
                                   connection_parameters)
        except AttributeError:
            self.thermal = None

        try:
            self.power = Power(self.get_link_url('Power'),
                               connection_parameters)
        except AttributeError:
            self.Power = None

    def get_type(self):
        '''Get chassis type

        :returns: chassis type or "Not available"
        :rtype: string

        '''
        try:
            return self.data.NetworkAdaptersType
        except AttributeError:
            return "Not available"


class Thermal(Base):
    '''Class to manage redfish Thermal data.'''
    def get_temperatures(self):
        '''Get chassis sensors name and temparature

        :returns: chassis sensor and temperature
        :rtype: dict

        '''
        temperatures = {}

        try:
            for sensor in self.data.Temperatures:
                temperatures[sensor.Name] = sensor.ReadingCelsius
            return temperatures
        except AttributeError:
            return "Not available"

    def get_fans(self):
        '''Get chassis fan name and rpm

        :returns: chassis fan and rpm
        :rtype: dict

        '''
        fans = {}

        try:
            for fan in self.data.Fans:
                fans[fan.FanName] = fan.ReadingRPM
            return fans
        except AttributeError:
            return "Not available"


class Power(Base):
    '''Class to manage redfish Power data.'''
    pass
