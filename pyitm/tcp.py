from twisted.protocols.portforward import ProxyClient, ProxyClientFactory
from twisted.protocols.portforward import ProxyServer, ProxyFactory as ProxyServerFactory


class TcpProxyClient(ProxyClient):

    def __init__(self):
        self.taps = []

    def dataReceived(self, data):
        for tap in self.taps:
            data = tap.onServerData(self.peer.transport.client, data)
            if data is None:
                print(f"WARNING: received data was dropped by tap '{tap}'")
                return
        super(ProxyClient, self).dataReceived(data)

    def connectionMade(self):
        super(TcpProxyClient, self).connectionMade()
        self.taps = self.peer.factory.taps
        for tap in self.taps:
            tap.onConnected(self.peer.transport.client)


class TcpProxyClientFactory(ProxyClientFactory):
    protocol = TcpProxyClient


class TcpProxyServer(ProxyServer):

    clientProtocolFactory = TcpProxyClientFactory

    def __init__(self):
        self.taps = []

    def connectionMade(self):
        self.taps = self.factory.taps
        super(TcpProxyServer, self).connectionMade()

    def connectionLost(self, reason):
        super(TcpProxyServer, self).connectionLost(reason)
        for tap in self.taps:
            tap.onDisconnected(self.transport.client)

    def dataReceived(self, data):
        for tap in self.taps:
            data = tap.onClientData(self.transport.client, data)
            if data is None:
                print(f"WARNING: received data was dropped by tap '{tap}'")
                return
        super(ProxyServer, self).dataReceived(data)


class TcpProxyServerFactory(ProxyServerFactory):
    protocol = TcpProxyServer

    def __init__(self, host, port, taps):
        super(TcpProxyServerFactory, self).__init__(host, port)
        self.taps = taps