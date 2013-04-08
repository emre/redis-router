# -*- coding: utf8 -*-

from redis_router.tcp_interface import RouterServer

r = RouterServer('0.0.0.0', 5000)
r.run()

"""
$ telnet localhost 5000
Trying 127.0.0.1...
Connected to localhost.
Escape character is '^]'.
set selam timu
True
get selam
timu
dbsize
13
"""