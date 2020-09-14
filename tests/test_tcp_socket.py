from unittest import TestCase

from pygoridge.socket_relay import SocketType
from test_rpc import CommonTests


class TCPSocketTest(TestCase, CommonTests):
    
    SOCK_ADDR = "127.0.0.1"
    SOCK_PORT = 7079
    SOCK_TYPE = SocketType.SOCK_TCP
