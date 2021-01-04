import requests
import json
import time
from pathlib import Path

class _urlscan():
    url = "https://urlscan.io/api/v1"

    def __init__(self, apiToken, ca=None, requestTimeout=30):
        self.requestTimeout = requestTimeout
        self.apiToken = apiToken
        self.headers = {
            "API-Key" : "{0}".format(self.apiToken)
        }
        if ca:
            self.ca = Path(ca)
        else:
            self.ca = None

    def apiCall(self,endpoint,methord="GET",data=None):
        kwargs={}
        kwargs["timeout"] = self.requestTimeout
        kwargs["headers"] = self.headers
        if self.ca:
            kwargs["verify"] = self.ca
        try:
            url = "{0}/{1}".format(self.url,endpoint)
            if methord == "GET":
                response = requests.get(url, **kwargs)
            elif methord == "POST":
                kwargs["data"] = data
                response = requests.post(url, **kwargs)
            elif methord == "DELETE":
                response = requests.delete(url, **kwargs)
        except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
            return 0, "Connection Timeout"
        if response.status_code == 200 or response.status_code == 202:
            return json.loads(response.text), response.status_code
        return None, response.status_code

    def submitURL(self,url,visibility="unlisted",tags=[]):
        data = { "url" : url, "visibility" : visibility, "tags" : tags }
        response, statusCode = self.apiCall("scan",methord="POST",data=data)
        if response["message"] == "Submission successful":
            return response["uuid"]
        return response

    def getResult(self,uuid,wait=False):
        response, statusCode = self.apiCall("result/{0}/".format(uuid))
        if statusCode == 404:
            if wait:
                while True:
                    time.sleep(2)
                    response, statusCode = self.apiCall("result/{0}/".format(uuid))
                    if statusCode == 200:
                        return response
            else:
                return { "msg" : "Scan not found may still be running?" }
        elif statusCode == 200:
            return response
        return None

    def searchScans(self,query,size=100,search_after=None):
        if search_after:
            response, statusCode = self.apiCall("search/?q={0}&size={1}&search_after={2}".format(query,size,search_after))
            return response
        response, statusCode = self.apiCall("search/?q={0}&size={1}".format(query,size))
        return response
