import datetime
import random
from unittest import TestCase

from pygoridge.constants import BUFFER_SIZE, PayloadType
from pygoridge.exceptions import ServiceException
from pygoridge.socket_relay import SocketType, SocketRelay
from pygoridge.rpc import RPC


class CommonTests:

    SOCK_ADDR = "0.0.0.0"
    SOCK_PORT = 7079
    SOCK_TYPE = SocketType.SOCK_TCP

    def make_relay(self):
        return SocketRelay(self.SOCK_ADDR, self.SOCK_PORT, self.SOCK_TYPE)

    def make_rpc(self):
        return RPC(self.make_relay())
        
    def test_manual_connect(self):
        relay = self.make_relay()
        conn = RPC(relay)

        self.assertFalse(relay.is_connected)

        relay.connect()
        self.assertTrue(relay.is_connected)

        self.assertEqual("pong", conn("Service.Ping", "ping"))
        self.assertTrue(relay.is_connected)

    def test_reconnect(self):
        relay = self.make_relay()
        conn = RPC(relay)

        self.assertFalse(relay.is_connected)
        self.assertEqual("pong", conn("Service.Ping", "ping"))
        self.assertTrue(relay.is_connected)

        relay.close()
        self.assertFalse(relay.is_connected)

        self.assertEqual("pong", conn("Service.Ping", "ping"))
        self.assertTrue(relay.is_connected)

    def test_ping_pong(self):
        conn = self.make_rpc()
        self.assertEqual("pong", conn("Service.Ping", "ping"))

    def test_ping_null(self):
        conn = self.make_rpc()
        self.assertEqual("", conn("Service.Ping", "not-ping"))

    def test_negate(self):
        conn = self.make_rpc()
        self.assertEqual(-10, conn("Service.Negate", 10))

    def test_negate_negative(self):
        conn = self.make_rpc()
        self.assertEqual(10, conn("Service.Negate", -10))

    def test_long_echo(self):
        conn = self.make_rpc()
        payload = "a" * BUFFER_SIZE * 5

        resp = conn("Service.Echo", payload)

        self.assertEqual(len(payload), len(resp))
        self.assertEqual(payload, resp)

    def test_convert_exception(self):
        conn = self.make_rpc()
        payload = "a" * BUFFER_SIZE * 5

        with self.assertRaises(ServiceException):
            resp = conn("Service.Echo", payload, flags=PayloadType.PAYLOAD_RAW)

    def test_raw_body(self):
        conn = self.make_rpc()
        payload = bytearray(random.getrandbits(8) for _ in range(100))

        resp = conn("Service.EchoBinary", payload, flags=PayloadType.PAYLOAD_RAW)

        self.assertEqual(len(payload), len(resp))
        self.assertEqual(payload, resp)

    def test_raw_body_bytes(self):
        conn = self.make_rpc()
        payload = b'\x01\x02\x03\x04\x05'

        resp = conn("Service.EchoBinary", payload, flags=PayloadType.PAYLOAD_RAW)

        self.assertEqual(len(payload), len(resp))
        self.assertEqual(payload, resp)

    def test_long_raw_body(self):
        conn = self.make_rpc()
        payload = bytearray(random.getrandbits(8) for _ in range(BUFFER_SIZE * 5))

        resp = conn("Service.EchoBinary", payload, flags=PayloadType.PAYLOAD_RAW)

        self.assertEqual(len(payload), len(resp))
        self.assertEqual(payload, resp)

    def test_payload(self):
        conn = self.make_rpc()

        resp = conn("Service.Process", {"name": "wolfy-j", "value": 18})
        self.assertEqual({"name": "WOLFY-J", "value": -18}, resp)

    def test_bad_payload(self):
        conn = self.make_rpc()
        msg = "{rawData} request for <*main.Payload Value>"
        with self.assertRaises(ServiceException) as e:
            resp = conn("Service.Process", "raw", flags=PayloadType.PAYLOAD_RAW)
            self.assertTrue(msg in str(e))

    def test_payload_with_map(self):
        conn = self.make_rpc()
        resp = conn("Service.Process", 
            {
            "name": "wolfy-j", 
            "value": 18,
            "keys": {"key": "value", "email": "domain"}
            })
        self.assertTrue(isinstance(resp["keys"], dict))
        self.assertEqual(resp["keys"]["value"], "key")
        self.assertEqual(resp["keys"]["domain"], "email")

    def test_broken_payload_map(self):
        conn = self.make_rpc()
        with self.assertRaises(ServiceException):
            resp = conn("Service.Process", 
                {
                "name": "wolfy-j", 
                "value": 18,
                "keys": 1111
                })

    def test_json_exception(self):
        conn = self.make_rpc()
        msg = "is not JSON serializable"
        with self.assertRaises(ServiceException) as e:
            resp = conn("Service.Process", bytes())
            self.assertTrue(msg in str(e))


class RPCTest(TestCase, CommonTests):
    pass