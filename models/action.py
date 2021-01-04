from core.models import action
from core import auth, db, helpers

from plugins.urlscan.includes import urlscan

class _urlscanSubmitURL(action._action):
    apiToken = str()
    url = str()
    visibility = str()

    def run(self,data,persistentData,actionResult):
        url = helpers.evalString(self.url,{"data" : data})
        visibility = helpers.evalString(self.visibility,{"data" : data})
        apiToken = auth.getPasswordFromENC(self.apiToken)

        if visibility == "":
            visibility = "unlisted"
      
        result = urlscan._urlscan(apiToken).submitURL(url,visibility)

        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["uuid"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 404
            actionResult["msg"] = "Failed to get a valid response from urlscan API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_urlscanSubmitURL,self).setAttribute(attr,value,sessionData=sessionData)

class _urlscanGetResult(action._action):
    apiToken = str()
    uuid = str()
    wait = bool()

    def run(self,data,persistentData,actionResult):
        uuid = helpers.evalString(self.uuid,{"data" : data})
        apiToken = auth.getPasswordFromENC(self.apiToken)
      
        result = urlscan._urlscan(apiToken).getResult(uuid,self.wait)

        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["apiResult"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 404
            actionResult["msg"] = "Failed to get a valid response from urlscan API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_urlscanGetResult,self).setAttribute(attr,value,sessionData=sessionData)

class _urlscanSearchScans(action._action):
    apiToken = str()
    searchQuery = str()
    searchAfter = str()
    size = int()

    def run(self,data,persistentData,actionResult):
        searchQuery = helpers.evalString(self.searchQuery,{"data" : data})
        searchAfter = helpers.evalString(self.searchAfter,{"data" : data})
        apiToken = auth.getPasswordFromENC(self.apiToken)
      
        result = urlscan._urlscan(apiToken).searchScans(searchQuery,size,searchAfter)

        if result:
            actionResult["result"] = True
            actionResult["rc"] = 0
            actionResult["apiResult"] = result
        else:
            actionResult["result"] = False
            actionResult["rc"] = 404
            actionResult["msg"] = "Failed to get a valid response from urlscan API"
        return actionResult 

    def setAttribute(self,attr,value,sessionData=None):
        if attr == "apiToken" and not value.startswith("ENC "):
            if db.fieldACLAccess(sessionData,self.acl,attr,accessType="write"):
                self.apiToken = "ENC {0}".format(auth.getENCFromPassword(value))
                return True
            return False
        return super(_urlscanSearchScans,self).setAttribute(attr,value,sessionData=sessionData)