import sys
import socket

from twisted.internet import reactor
from pyitm.example_taps import PrintTap, ReReplaceTap
from pyitm.main import setupPyITMUdp


if len(sys.argv) != 4:
    print(f"usage: {sys.argv[0]} <upstream dns host/ip> <search IP> <replace IP>")
    sys.exit(1)

dst_hostname = sys.argv[1]
dst_host = socket.gethostbyname(dst_hostname)
dst_port = 53
listen_port = 53053

searchip_packed = socket.inet_pton(socket.AF_INET, sys.argv[2])
replaceip_packed = socket.inet_pton(socket.AF_INET, sys.argv[3])

mytaps = [PrintTap("[ORIGINAL]", verbose=False),
          ReReplaceTap(searchip_packed, replaceip_packed),
          PrintTap("[MODIFIED]")]
setupPyITMUdp(mytaps, dst_host, dst_port, bind_port=listen_port)
print(f"Listening on port {listen_port}")
reactor.run()
