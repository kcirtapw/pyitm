from .tcp import TcpProxyServerFactory
from .udp import UdpProxyServer


class Tap:

    def onClientData(self, client_addr, data):
        return data

    def onServerData(self, client_addr, data):
        return data

    def onConnected(self, client_addr):
        pass

    def onDisconnected(self, client_addr):
        pass


def setupPyITMTcp(taps, dst_host, dst_port, bind_port=None, bind_host=None, reactor=None):
    if reactor is None:
        from twisted.internet import reactor
    if bind_port is None:
        bind_port = dst_port
    reactor.listenTCP(bind_port, TcpProxyServerFactory(dst_host, dst_port, taps))


def setupPyITMUdp(taps, dst_host, dst_port, bind_port=None, bind_host=None, reactor=None):
    if reactor is None:
        from twisted.internet import reactor
    if bind_port is None:
        bind_port = dst_port
    reactor.listenUDP(bind_port, UdpProxyServer(dst_host, dst_port, taps))

