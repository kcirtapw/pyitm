import sys
import socket

from twisted.internet import reactor
from pyitm.example_taps import PrintTap, ReReplaceTap
from pyitm import setupPyITMTcp


if len(sys.argv) != 3:
    print(f"usage: {sys.argv[0]} <destination host/ip> <destination port>")
    sys.exit(1)

dst_hostname = sys.argv[1]
dst_host = socket.gethostbyname(dst_hostname)
dst_port = int(sys.argv[2])
listen_port = 8081

mytaps = [PrintTap("[ORIGINAL]", verbose=False),
          ReReplaceTap(f"\r\nHost: localhost:{listen_port}\r\n".encode('utf-8'),
                       f"\r\nHost: {dst_hostname}:{dst_port}\r\n".encode('utf-8')),
          ReReplaceTap(b"\r\nAccept-Encoding: gzip, deflate\r\n", b"\r\n"),
          ReReplaceTap(b"\r\nIf-Modified-Since: .+\r\n", b"\r\n"),
          PrintTap("[MODIFIED]")]
setupPyITMTcp(mytaps, dst_host, dst_port, bind_port=listen_port)
print(f"Listening on port {listen_port}")
reactor.run()
