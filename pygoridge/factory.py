import re
import sys

from pygoridge.exceptions import RelayFactoryException
from pygoridge.relay import Relay
from pygoridge.stream_relay import StreamRelay
from pygoridge.socket_relay import SocketRelay, SocketType


CONNECTION_PATTERN = re.compile(
    f"({Relay.STREAM}|(?P<protocol>({Relay.TCP_SOCKET}|{Relay.UNIX_SOCKET})):\/\/(?P<address>[^:]+)(:(?P<port>[^:]+))?)",
    re.IGNORECASE
)


def create_relay(connection: str) -> Relay:
    m = CONNECTION_PATTERN.match(connection)
    if not m:
        raise RelayFactoryException(
            f"unknown connection specification: {connection}")

    if m.string == Relay.STREAM:
        return StreamRelay(sys.stdin.buffer.raw, sys.stdout.buffer.raw)
    elif m.group("protocol") == Relay.TCP_SOCKET:
        try:
            port = int(m.group("port"))
        except (TypeError, ValueError):
            raise RelayFactoryException(
                f"wrong port number in connection specification: {connection}")
        return SocketRelay(
                    m.group("address"),
                    port=port,
                    socket_type=SocketType.SOCK_TCP)
    elif m.group("protocol") == Relay.UNIX_SOCKET:
        return SocketRelay(
            m.group("address"), socket_type=SocketType.SOCK_UNIX)

    raise RelayFactoryException(
            f"unknown connection specification: {connection}")
