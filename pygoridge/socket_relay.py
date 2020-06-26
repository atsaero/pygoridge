import io
from typing import Optional

from pygoridge.exceptions import (PrefixException, TransportException, 
    InvalidArgumentException, RelayException)
from pygoridge.relay import Relay


class SocketType:
    SOCK_TCP  = 0
    SOCK_UNIX = 1


class SocketRelay(Relay):

    def __init__(self, address: str, port: Optional[int] = None, 
                 socket_type: int = SocketType.SOCK_TCP):
        if socket_type == SocketType.SOCK_TCP:
            if port is None or 65535 < port < 1:
                raise InvalidArgumentException(f"no port given for TPC socket on {address}")
        elif socket_type == SocketType.SOCK_UNIX:
            pass
        else:
            raise InvalidArgumentException(f"undefined connection type {socket_type} on '{address}'")

        self._address = address
        self._port = port
        self._socket_type = socket_type
        self._sock = None

    def __str__(self):
        if self._socket_type == SocketType.SOCK_TCP:
            return f"tcp://{self._address}:{self._port}"
        elif self._socket_type == SocketType.SOCK_UNIX:
            return f"unix://{self._address}"

    def __del__(self):
        if self.is_connected:
            self.close()

    def is_connected(self):
        return self._sock is not None

    @property
    def address(self) -> str:
        return self._address

    @property
    def port(self) -> Optional[str]:
        return self._port
    
    @property
    def socket_type(self) -> int:
        return self._socket_type

    def send_package(self, header_payload: str, body_payload: str,
                     header_flags: Optional[int] = None, 
                     body_flags: Optional[int] = None) -> 'SocketRelay':
        self._connect()
        return super().send_package(header_payload=header_payload, 
            body_payload=body_payload, header_flags=header_flags, body_flags=body_flags)

    def send(self, payload: str, flags: Optional[int] = None) -> 'SocketRelay':
        self._connect()
        return super().send(payload, flags)

    def close(self):
        if not self.is_connected:
            raise RelayException(f"unable to close socket '{self}', socket already closed")
        self._sock.close()
        self._sock = None

    def _read(self, buffer: memoryview) -> int:
        view = buffer
        size = 0
        try:
            while len(view):
                n = self._sock.recv_into(view)
                view = view[n:] 
                size += n
        except Exception as e:
            raise TransportException(f"unable to read from socket {self}")
        return size

    def _write(self, buffer: memoryview):
        try:
            self._sock.sendall(buffer)
        except Exception as e:
            raise TransportException(f"unable to write to socket {self}")

    def _connect(self):
        if self.is_connected:
            return
        try:
            if self._socket_type == SocketType.SOCK_TCP:
                self._sock = socket.create_connection((self._address, self._port), timeout=10)
                self._sock.settimeout(None)
            elif self._socket_type == SocketType.SOCK_UNIX:
                self._sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
                self._sock.connect(self._address)
        except Exception as e:
            raise TransportException(f"unable to establish connection {self}: {str(e)}")
