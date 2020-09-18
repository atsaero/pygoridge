from unittest import TestCase

from pygoridge import SocketRelay
from pygoridge.exceptions import InvalidArgumentException


class SocketRelayTest(TestCase):

    def test_socket_relay_init(self):
        invalid_args = [
            # unknown type
            ['localhost', 8080, 8080],
            # invalid ports
            ['localhost', None, 0],
            ['localhost', 66666, 0]
        ]
        valid_args = [
            # ok
            ['localhost', 66666, 1],
            ['localhost', 8080, 0]
        ]
        for invalid in invalid_args:
            with self.assertRaises(InvalidArgumentException):
                SocketRelay(*invalid)
        for valid in valid_args:
            SocketRelay(*valid)
