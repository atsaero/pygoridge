import json
import socket
from unittest import TestCase


class WorkerTest(TestCase):

    SOCK_ADDR = "0.0.0.0"
    SOCK_PORT = 7080

    def test_echo(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.SOCK_ADDR, self.SOCK_PORT))
        payload = b'Hello, world\n'
        s.sendall(payload)
        data = s.recv(1024)
        s.close()
        assert data == payload

    def test_context(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((self.SOCK_ADDR, self.SOCK_PORT))
        payload = b'context\n'
        s.sendall(payload)
        data = s.recv(1024)
        s.close()
        context = json.loads(data)
        assert context["worker"] == "python"
        assert "remote" in context
