# coding=utf-8

redfish_mapper = None

class RedfishVersionMapping(object):
    """Implements basic url path mapping beetween Redfish versions."""

    def __init__(self, version):
        self.__version = version

    def map_sessionservice(self):
        if self.__version == "0.9.5":
            return "Sessions"
        if self.__version == "0.96.0":
            return "SessionService"
        return("SessionService")
        

    def map_links(self):
        if self.__version == "0.9.5":
            return "links"
        if self.__version == "0.96.0":
            return "Links"
        return("Links")
        

    def map_links_ref(self):
        if self.__version == "0.9.5":
            return "href"
        if self.__version == "0.96.0":
            return "@odata.id"
        return("@odata.id")
    
    def map_members(self):
        if self.__version == "0.9.5":
            return "Member"
        if self.__version == "0.96.0":
            return "Members"
        return("Members")