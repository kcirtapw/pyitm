import sys
import socket
import cmd
from threading import Thread

from twisted.internet import reactor
from pyitm.example_taps import PrintTap, ReReplaceTap
from pyitm.main import setupPyITMUdp


if len(sys.argv) != 4:
    print(f"usage: {sys.argv[0]} <upstream dns host/ip> <search IP> <replace IP>")
    sys.exit(1)

dst_hostname = sys.argv[1]
dst_host = socket.gethostbyname(dst_hostname)
dst_port = 53
listen_port = 5352

searchip_packed = socket.inet_pton(socket.AF_INET, sys.argv[2])
replaceip_packed = socket.inet_pton(socket.AF_INET, sys.argv[3])

replacetap = ReReplaceTap(searchip_packed, replaceip_packed)
mytaps = [PrintTap("[ORIGINAL]", verbose=False),
          replacetap,
          PrintTap("[MODIFIED]")]


class PyITMInteractive(cmd.Cmd):
    prompt = "pyitm:example_udp_interactive > "

    def do_activate(self, _):
        '''Activate the ReReplaceTap'''
        replacetap.active = True
        print("activated module ReReplaceTap")

    def do_deactivate(self, _):
        '''Deactivate the ReReplaceTap'''
        replacetap.active = False
        print("deactivated module ReReplaceTap")

    def do_status(self, _):
        '''Print a short status'''
        status = "active" if replacetap.active else "inactive"
        print(f"Module ReReplaceTap is {status}")

    def precmd(self, line: str) -> str:
        if line is not None:
            line = line.strip().lower()
        if line is None or line == "":
            line = "status"
        return super(PyITMInteractive, self).precmd(line)

setupPyITMUdp(mytaps, dst_host, dst_port, bind_port=listen_port)
print(f"Listening on port {listen_port}")

reactorThread = Thread(target=lambda: reactor.run(installSignalHandlers=0), daemon=True)
reactorThread.start()
try:
    PyITMInteractive().cmdloop()
except KeyboardInterrupt:
    reactor.stop()
