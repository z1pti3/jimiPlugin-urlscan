from core import plugin, model

class _urlscan(plugin._plugin):
    version = 0.1

    def install(self):
        # Register models
        model.registerModel("urlscanSubmitURL","_urlscanSubmitURL","_action","plugins.urlscan.models.action")
        model.registerModel("urlscanGetResult","_urlscanGetResult","_action","plugins.urlscan.models.action")
        model.registerModel("urlscanSearchScans","_urlscanSearchScans","_action","plugins.urlscan.models.action")
        return True

    def uninstall(self):
        # deregister models
        model.deregisterModel("urlscanSubmitURL","_urlscanSubmitURL","_action","plugins.urlscan.models.action")
        model.deregisterModel("urlscanGetResult","_urlscanGetResult","_action","plugins.urlscan.models.action")
        model.deregisterModel("urlscanSearchScans","_urlscanSearchScans","_action","plugins.urlscan.models.action")
        return True

    def upgrade(self,LatestPluginVersion):
        pass
        #if self.version < 0.2:
