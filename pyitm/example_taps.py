import re
from pyitm.main import Tap


class PrintTap(Tap):
    def __init__(self, prefix="[TAP] ", verbose=True):
        self.prefix = prefix
        self.verbose = verbose

    def onConnected(self, client_addr):
        if self.verbose:
            print(f"{self.prefix}[{client_addr[0]}:{client_addr[1]}] intercepted connection established")

    def onDisconnected(self, client_addr):
        if self.verbose:
            print(f"{self.prefix}[{client_addr[0]}:{client_addr[1]}] connection lost")

    def onClientData(self, client_addr, data):
        print(f"{self.prefix}[{client_addr[0]}:{client_addr[1]}] > {data}")
        return data

    def onServerData(self, client_addr, data):
        print(f"{self.prefix}[{client_addr[0]}:{client_addr[1]}] < {data}")
        return data


class ReReplaceTap(Tap):
    def __init__(self, search, replace, count=0, active=True):
        self.pattern = re.compile(search)
        self.replace = replace
        self.count = count
        self.active = active

    def onClientData(self, client_addr, data):
        if self.active:
            return self.pattern.sub(self.replace, data, self.count)
        else:
            return data

    def onServerData(self, client_addr, data):
        if self.active:
            return self.pattern.sub(self.replace, data, self.count)
        else:
            return data
