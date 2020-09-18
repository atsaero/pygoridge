import io

from pygoridge.exceptions import TransportException, InvalidArgumentException
from pygoridge.relay import Relay


class StreamRelay(Relay):

    def __init__(self, input_stream: io.RawIOBase,
                 output_stream: io.RawIOBase):

        if not input_stream.readable():
            raise InvalidArgumentException("`input_stream` must be readable")

        if not output_stream.writable():
            raise InvalidArgumentException("`output_stream` must be writable")

        self._in = input_stream
        self._out = output_stream

    def close(self):
        return

    def _read(self, buffer: memoryview) -> int:
        try:
            read_bytes = self._in.read(len(buffer))
        except Exception as e:
            raise TransportException(
                f"error reading payload from the stream: {str(e)}")

        if read_bytes is None:
            raise TransportException("error reading payload from the stream")
        buffer[:len(read_bytes)] = read_bytes
        return len(read_bytes)

    def _write(self, buffer: memoryview):
        try:
            if self._out.write(buffer) is None:
                raise TransportException(
                    "no single byte could be readily written to stream")
        except Exception as e:
            raise TransportException(
                f'unable to write payload to the stream: {str(e)}')
