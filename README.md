An easy to use, TCP and UDP level Man-in-the-middle framework intended for security researchers and practitioners.

It provides a simple interface for creating and putting together mitm modules - so-called taps.
They can be put together in a chain, individually taking care of just one part of one's inspection of modification needs.
It uses the same interface for TCP and UDP taps, so modules can be reused if applicable.

This module __does not__ take care of redirecting the traffic to it.
It is intended to provide a lightweight but general purpose framework for implementing inspection or modification modules only.
The users of this software need to take care getting traffic into it, e.g. by ARP-spoofing, iptables, etc.

## Installation

PyITM can be easily installed from pypi with all dependencies via e.g. pip:
```
pip install pyitm
```

## Usage

TBD
<!--
- Implement a tap
- start listening with `setupPyITMUdp` or `setupPyITMTcp`
-->
 

## Examples

**TCP:**

_See `examples/example_tcp.py` for implementation._

This example forwards HTTP traffic (actually, any TCP traffic) to a destination host/port given on the command line and will do the following tasks:
- Log packets on stdout before and after modification
- Update the "Host:" header to match the target (most webservers nowadays do not serve the correct page if it is not set properly)
- Remove the "Accept-Encoding" header, so the response will not be gziped or deflated
- Remove the "If-Modified-Since:" header, so the server will always send the full response



Running the example and opening the URL http://localhost:8081/ in a browser:

```
$ python examples/example_tcp.py neverssl.com 80
Listening on port 8081
[ORIGINAL][127.0.0.1:35028] intercepted connection established
[ORIGINAL][127.0.0.1:35028] > b'GET / HTTP/1.1\r\nHost: localhost:8081\r\nUser-Agent: Mozilla/5.0 [...]'
[MODIFIED][127.0.0.1:35028] > b'GET / HTTP/1.1\r\nHost: neverssl.com:80\r\nUser-Agent: Mozilla/5.0 [...]'
[ORIGINAL][127.0.0.1:35028] < b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 2536[...]'
[MODIFIED][127.0.0.1:35028] < b'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 2536[...]'
[ORIGINAL][127.0.0.1:35028] < b'<html>\n    <head>\n        <title>NeverSSL - helping you get online[...]'
[MODIFIED][127.0.0.1:35028] < b'<html>\n    <head>\n        <title>NeverSSL - helping you get online[...]'
```


**UDP:**

_See `examples/example_udp.py` for implementation._

This example forwards DNS traffic (actually, any UDP traffic) to a destination host/port given on the command line and will do the following tasks:
- Log packets on stdout before and after modification
- In a packet, replace a given IP address with another one, both given as command line options

Running the example:
```
$ python examples/example_udp.py 192.168.1.1 46.38.239.190 127.0.0.1
Listening on port 53053
```

Connecting with a sample client:
```
$ dig -p53053 +short alles.anzünden.jetzt  @127.0.0.1
127.0.0.1
```

Tool output:
```
[ORIGINAL][127.0.0.1:48431] connection interception established
[ORIGINAL][127.0.0.1:48431] > b'\x90\xbf\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x05alles\x0fxn--anznden-p2a\x05jetzt\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xab-Rh\x1e\x9c2\xed'
[MODIFIED][127.0.0.1:48431] > b'\x90\xbf\x01 \x00\x01\x00\x00\x00\x00\x00\x01\x05alles\x0fxn--anznden-p2a\x05jetzt\x00\x00\x01\x00\x01\x00\x00)\x10\x00\x00\x00\x00\x00\x00\x0c\x00\n\x00\x08\xab-Rh\x1e\x9c2\xed'
[ORIGINAL][127.0.0.1:48431] < b'\x90\xbf\x81\x80\x00\x01\x00\x01\x00\x00\x00\x01\x05alles\x0fxn--anznden-p2a\x05jetzt\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x0bg\x00\x04.&\xef\xbe\x00\x00)\x02\x00\x00\x00\x00\x00\x00\x00'
[MODIFIED][127.0.0.1:48431] < b'\x90\xbf\x81\x80\x00\x01\x00\x01\x00\x00\x00\x01\x05alles\x0fxn--anznden-p2a\x05jetzt\x00\x00\x01\x00\x01\xc0\x0c\x00\x01\x00\x01\x00\x00\x0bg\x00\x04\x7f\x00\x00\x01\x00\x00)\x02\x00\x00\x00\x00\x00\x00\x00'
```


**Interactive:**

_See `examples/example_udp_interactive.py` for implementation._

This example is very similar to `example_udp.py` but gives the user an interactive text console to change the tool's behaviour during runtime.
It is intended to demonstrate how interaction with the taps during runtime can be implemented.