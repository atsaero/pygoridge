from unittest import TestCase

from pygoridge import SocketType, RPC
from test_rpc import CommonTests


class TCPSocketTest(TestCase, CommonTests):

    SOCK_ADDR = "127.0.0.1"
    SOCK_PORT = 7079
    SOCK_TYPE = SocketType.SOCK_TCP

    def test_context_manager(self):
        with self.make_relay() as relay:
            conn = RPC(relay)
            self.assertTrue(relay.is_connected)
            self.assertEqual("pong", conn("Service.Ping", "ping"))
            self.assertTrue(relay.is_connected)

        self.assertFalse(relay.is_connected)
