# coding=utf-8

class RedfishVersionMapping(object):
    """Implements basic url path mapping beetween Redfish versions."""

    def __init__(self, version):
        self._version = version

    def map_sessions(self):
        if self._version == "0.9.5":
            return "Sessions"
        if self._version == "0.96.0":
            return "SessionService"

    def map_links(self):
        if self._version == "0.9.5":
            return "links"
        if self._version == "0.96.0":
            return "Links"

    def map_links_ref(self):
        if self._version == "0.9.5":
            return "href"
        if self._version == "0.96.0":
            return "@odata.id"