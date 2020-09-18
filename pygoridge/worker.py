import os
from typing import Optional, Union, Any

from pygoridge.constants import PayloadType, WORKER_STOP_MESSAGE
from pygoridge.exceptions import WorkerException
from pygoridge.json import json_loads, json_dumps
from pygoridge.relay import Relay


class Worker:

    def __init__(
                 self,
                 relay: Relay,
                 json_encoder=json_dumps,
                 json_decoder=json_loads):
        self._relay = relay
        self._json_decoder = json_decoder
        self._json_encoder = json_encoder

    def receive(self) -> (Optional[memoryview], Optional[memoryview]):
        return self._receive()

    def _receive(
                 self,
                 header: Optional[Union[str, Any]] = None
                 ) -> (Optional[memoryview], Optional[memoryview]):
        received_bytes, flags = self._relay.receive_sync()

        if flags & PayloadType.PAYLOAD_CONTROL:
            proceed, header = self._handle_control(received_bytes, flags)
            if proceed:
                # wait for the next command, passing the last received header
                return self._receive(header)
            else:
                # Expect process termination
                return None, None

        if flags & PayloadType.PAYLOAD_ERROR:
            raise WorkerException(
                f'got error: {received_bytes.decode("utf-8")}')

        # return the last received header (through control) if any, and body
        return header, received_bytes

    def send(self, payload: Optional[Union[bytes, memoryview]] = None,
             header: Optional[Union[str, Any]] = None):
        if header is None:
            header_data = ""
        elif not isinstance(header, str):
            header_data = self._json_encoder(header)

        header_data = header_data.encode("utf-8")
        payload = memoryview(payload or b"")

        if header is None:
            header_flags = PayloadType.PAYLOAD_CONTROL | PayloadType.PAYLOAD_NONE
        else:
            header_flags = PayloadType.PAYLOAD_CONTROL | PayloadType.PAYLOAD_RAW

        self._relay.send(header_data, header_flags)
        self._relay.send(payload, PayloadType.PAYLOAD_RAW)

    def error(self, message: str):
        self._relay.send(
            memoryview(message.encode("utf-8")),
            PayloadType.PAYLOAD_CONTROL | PayloadType.PAYLOAD_RAW | PayloadType.PAYLOAD_ERROR
        )

    def stop(self):
        self.send(header=WORKER_STOP_MESSAGE)

    def _handle_control(
            self,
            received_bytes: Optional[memoryview] = None,
            flags: int = 0) -> (bool, Union[memoryview, Any]):

        if received_bytes is None or flags & PayloadType.PAYLOAD_RAW:
            return True, received_bytes

        try:
            p = self._json_decoder(received_bytes.tobytes())
        except Exception as e:
            raise WorkerException(
                f"invalid task context, JSON payload is expected: {str(e)}")

        # PID negotiation (for pipes)
        if p.get("pid"):
            pid_msg = '{"pid":%s}' % os.getpid()
            self._relay.send(
                memoryview(pid_msg.encode("utf-8")), PayloadType.PAYLOAD_CONTROL
            )

        if p.get("stop"):
            return False, p

        return True, p
