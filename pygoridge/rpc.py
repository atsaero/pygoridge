import struct
from typing import Optional, Union, Any

from pygoridge.constants import PREFIX_LENGTH, PayloadType
from pygoridge.exceptions import ServiceException, TransportException
from pygoridge.json import json_dumps, json_loads
from pygoridge.relay import Relay


class RPC:

    def __init__(self, relay: Relay, json_encoder=json_dumps, json_decoder=json_loads):
        self._relay = relay
        self._seq = 0
        self._json_encoder = json_encoder
        self._json_decoder = json_decoder


    def __call__(method: str, payload, flags: Optional[int] = 0):
        method = method.encode("utf-8")
        header_size = len(method) + 8
        header = memoryview(bytearray(header_size))
        header[:len(method)] = method
        struct.pack_into('<Q', header, len(method), self._seq)

        self._relay.send(header, PayloadType.PAYLOAD_CONTROL | PayloadType.PAYLOAD_RAW)

        if flags & PayloadType.PAYLOAD_RAW and isinstance(payload, str):
            payload_data = payload.encode("utf-8")
            self._relay.send(payload_data, flags)
        else:
            try:
                body = self._json_encoder(payload).encode("utf-8")
            except Exception as e:
                raise ServiceException(f"error while encoding to json: {str(e)}")
            self._relay.send(body)

        response, flags = self._relay.receive_sync()

        if not flags & PayloadType.PAYLOAD_CONTROL:
            raise TransportException('rpc response header is missing')

        response_seq = struct.unpack('<Q', response[-8:])
        response_method = response[:-8].decode("utf-8")

        if response_seq != self._seq or response_method != method:
            raise TransportException(f"rpc method call, expected {self._seq}:{method}, got {response_seq}:{response_method}")

        self._seq += 1

        return self._handle_body(self._relay.receive_sync())

    def _handle_body(self, body: memoryview, flags: int) -> Union[memoryview, Any]:
        if flags & PayloadType.PAYLOAD_ERROR and flags & PayloadType.PAYLOAD_RAW:
            raise ServiceException(f"error handling rpc response body")

        if flags & PayloadType.PAYLOAD_RAW:
            return body

        return self._json_decoder(memoryview.tobytes())
