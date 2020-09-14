from unittest import TestCase

from pygoridge.exceptions import RelayFactoryException
from pygoridge.factory import create_relay
from pygoridge.socket_relay import SocketRelay, SocketType
from pygoridge.stream_relay import StreamRelay


class RelayFactoryTest(TestCase):

    def test_format(self):
        formats = [
            #format invalid
            ['tcp:localhost:', True],
            ['tcp:/localhost:', True],
            ['tcp//localhost:', True],
            ['tcp//localhost', True],
            ['tcp://localhost', True],
            ['pipes://localhost:', True],
            ['pipes://localhost', True],
            ['pipes://stdin:test', True],
            ['pipes://test:stdout', True],
            ['pipes://test:test', True],
            ['tcp://localhost:abc', True],
            #unknown provider
            ['test://localhost', True],
            #valid format
            ['tcp://localhost:123', False],
            ['unix://localhost:123', False],
            ['unix://rpc.sock', False],
            ['unix:///tmp/rpc.sock', False],
            ['pipes', False],
        ]

        for connection_format, assert_exception in formats:
            if assert_exception:
                with self.assertRaises(RelayFactoryException):
                    relay = create_relay(connection_format)
            else:
                relay = create_relay(connection_format)


    def test_tcp(self):
        relay = create_relay("tcp://localhost:0")
        self.assertTrue(isinstance(relay, SocketRelay))
        self.assertEqual("localhost", relay.address)
        self.assertEqual(0, relay.port)
        self.assertEqual(SocketType.SOCK_TCP, relay.socket_type)

    def test_unix(self):
        relay = create_relay("unix:///tmp/rpc.sock")
        self.assertTrue(isinstance(relay, SocketRelay))
        self.assertEqual("/tmp/rpc.sock", relay.address)
        self.assertEqual(SocketType.SOCK_UNIX, relay.socket_type)

    def test_pipes(self):
        relay = create_relay("pipes")
        self.assertTrue(isinstance(relay, StreamRelay))
