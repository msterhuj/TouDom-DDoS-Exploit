from core.lib.static import ip_private
import requests

from core.manager.PluginManager import PluginManager


class Client:

    plugin_manager: PluginManager
    url: str
    scan_private: bool

    # add data dataDriver
    def __init__(self, plugins: PluginManager, url: str, scan_private=False):
        self.plugin_manager = plugins
        self.url = url
        self.scan_private = scan_private
        self.run()

    def scan(self, ip: str):
        for plugin in self.plugin_manager.plugins:
            plugin.scan(ip)
            # todo add return info to data driver

    def run(self):
        while True:
            r = requests.get(self.url + "/next")
            if r.text:
                if self.scan_private:
                    self.scan(r.text)
                else:
                    if r.text not in ip_private:
                        self.scan(r.text)
            else:
                exit(0)