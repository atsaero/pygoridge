from abc import ABC, abstractmethod

from pygoridge.constants import PREFIX_LENGTH, BUFFER_SIZE, PayloadType
from pygoridge.protocol import parse_prefix, pack_message


class Relay(ABC):

    TCP_SOCKET  = 'tcp'
    UNIX_SOCKET = 'unix'
    STREAM      = 'pipes'

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def _read(self, buffer: memoryview) -> int:
        pass

    @abstractmethod
    def _write(self, data: memoryview):
        pass

    def receive_sync(self) -> (memoryview, int):
        prefix = self._fetch_prefix()
        if prefix['size'] == 0:
            return b"", prefix['flags']

        buf = bytearray(prefix['size'])#bytearray(min(prefix['size'], BUFFER_SIZE))
        view = memoryview(buf)
        
        bytes_length = self._read(view)
        return view, prefix["flags"]

    def send(self, payload: memoryview, flags: int = 0) -> 'Relay':
        data = self._prepare_send(payload, flags)
        self._write(data)
        return self

    def _prepare_send(self, payload: memoryview, flags: int = 0) -> memoryview:
        package = pack_message(payload, flags)
        if package is None:
            raise TransportException('unable to send payload with PAYLOAD_NONE flag')

        return package['body'][:(PREFIX_LENGTH + package['size'])]    

    def _fetch_prefix(self) -> dict:
        prefix = bytearray(PREFIX_LENGTH)
        prefix_view = memoryview(prefix)
        self._read(prefix_view)
        return parse_prefix(prefix_view)
