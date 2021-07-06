from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor


class UdpProxyClient(DatagramProtocol):

    def __init__(self, serverproxy, peer_address):
        super(UdpProxyClient, self).__init__()
        self.serverproxy = serverproxy
        self.destination = self.serverproxy.destination
        self.peer_address = peer_address

    def startProtocol(self):
        self.transport.connect(*self.destination)
        for tap in self.serverproxy.taps:
            tap.onConnected(self.peer_address)

    def datagramReceived(self, data, addr):
        for tap in self.serverproxy.taps:
            data = tap.onServerData(self.peer_address, data)
            if data is None:
                print(f"WARNING: received data was dropped by tap '{tap}'")
                return
        self.serverproxy.transport.write(data, self.peer_address)

    def connectionRefused(self):
        print(f"WARNING: connection refused: udp://{self.destination[0]}:{self.destination[1]}")
        for tap in self.serverproxy.taps:
            tap.onDisconnected(self.peer_address)


class UdpProxyServer(DatagramProtocol):

    def __init__(self, dst_host, dst_port, taps):
        super(UdpProxyServer, self).__init__()
        self.clients = {}
        self.taps = taps
        self.destination = (dst_host, dst_port)

    def startClient(self, addr):
        clientproxy = UdpProxyClient(self, addr)
        reactor.listenUDP(0, clientproxy)
        self.clients[addr] = clientproxy
        return clientproxy

    def datagramReceived(self, data, addr):
        if addr not in self.clients:
            clientproxy = self.startClient(addr)
        else:
            clientproxy = self.clients[addr]

        for tap in self.taps:
            data = tap.onClientData(addr, data)
            if data is None:
                print(f"WARNING: received data was dropped by tap '{tap}'")
                return
        clientproxy.transport.write(data)
