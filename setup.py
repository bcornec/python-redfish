#!/usr/bin/env python
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# THIS FILE IS MANAGED BY THE GLOBAL REQUIREMENTS REPO - DO NOT EDIT
import os
import sys
import ConfigParser
import distutils.sysconfig
import setuptools

# In python < 2.7.4, a lazy loading of package `pbr` will break
# setuptools if some other modules registered functions in `atexit`.
# solution from: http://bugs.python.org/issue15881#msg170215
try:
    import multiprocessing  # noqa
except ImportError:
    pass


def getfiles(path):
    '''Retrieve file list within a directory

    :param path: directory path
    :type path: string
    :returns: file list
    :rtype: list
    '''
    for root, dirs, files in os.walk(path):
        file_list = [os.path.join(root, file) for file in files]
    return(file_list)


def isdebianbased():
    '''Check if it is a Debian based system

    :returns: True if debian based, false otherwise.
    :rtype: bool
    .. note:: This is defined by looking at the python path
       Currently I have not find a better way to find the correct installation
       path in such case.

       From : https://wiki.debian.org/Python
       distutils setup scripts install files in /usr/local/ not sys.prefix
       (which is normally /usr/). This is because /usr/ is reserved for files
       installed from Debian packages. Note that
       /usr/local/lib/pythonX.Y/dist-packages is in sys.path so that modules
       not installed from Debian packages can still be accessed by the system
       Python. Tools like debhelper pass the --install-layout=deb option to
       the setup script while building a Debian package so that its installs
       files into /usr/ not /usr/local/.

    '''
    if([x for x in sys.path if 'dist-package' in x]):
        return(True)
    else:
        return(False)


def check_conf_file_location():
    '''Retrieve data_files values for setuptools.setup()

    :returns: data_files value that can be used by setuptools.setup()
              like the following example.
              [('etc/', ['redfish-client/etc/redfish-client.conf']),
               ('share/redfish-client/templates',
                ['redfish-client/templates/manager_info.template',
                 'redfish-client/templates/bla.template'])]
    :rtype: structure compatible with setuptools.setup()
    '''
    file_location = []
    # Add conf file according to prefix
    if(distutils.sysconfig.PREFIX == '/usr' and not isdebianbased()):
        file_location.append(('/etc/',
                              getfiles('redfish-client/etc')))
    else:
        file_location.append(('etc/',
                              getfiles('redfish-client/etc')))
    # Add template files
    file_location.append(('share/redfish-client/templates',
                          getfiles('redfish-client/templates')))
    return(file_location)

# Install software
setuptools.setup(
    setup_requires=['pbr'],
    pbr=True,
    data_files=check_conf_file_location())

# Define conf file location
configfile_location = ''
templatedir_location = ''
for file_location in check_conf_file_location():
    if('etc' in file_location[1][0]):
        if(distutils.sysconfig.PREFIX == '/usr' and isdebianbased()):
            configfile_location = os.path.join(
                '/usr/local',
                file_location[0],
                os.path.basename(file_location[1][0]))
        elif('/etc/' in file_location[0]):
            configfile_location = os.path.join(
                file_location[0],
                os.path.basename(file_location[1][0]))
        else:
            configfile_location = os.path.join(
                distutils.sysconfig.PREFIX,
                file_location[0],
                os.path.basename(file_location[1][0]))
    elif('templates' in file_location[1][0]):
        if(distutils.sysconfig.PREFIX == '/usr' and isdebianbased()):
            templatedir_location = os.path.join(
                '/usr/local',
                file_location[0])
        else:
            templatedir_location = os.path.join(
                distutils.sysconfig.PREFIX,
                file_location[0])
# Update conf file
config = ConfigParser.ConfigParser()
config.read(configfile_location)
config.set('redfish-client', 'templates_path', templatedir_location)
with open(configfile_location, 'w') as configfile:
    config.write(configfile)

