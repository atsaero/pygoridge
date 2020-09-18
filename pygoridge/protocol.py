import struct
from typing import Optional

from pygoridge.constants import PREFIX_LENGTH, PayloadType
from pygoridge.exceptions import PrefixException


def pack_message(payload: memoryview, flags: int = 0) -> Optional[dict]:
    size = len(payload)

    if flags & PayloadType.PAYLOAD_NONE and size != 0:
        return

    buff = memoryview(bytearray(PREFIX_LENGTH + size))
    # unsigned char
    struct.pack_into('>B', buff, 0, flags)
    # unsigned long long (always 64 bit, little endian byte order)
    struct.pack_into('<Q', buff, 1, size)
    # unsigned long long (always 64 bit, big endian byte order) - checksum
    struct.pack_into('>Q', buff, 9, size)

    if not (flags is not None and flags & PayloadType.PAYLOAD_NONE):
        buff[PREFIX_LENGTH:] = payload
    return {'body': buff, 'size': size}


def parse_prefix(prefix: memoryview) -> dict:
    result = {}
    result['flags'] = struct.unpack_from('>B', prefix)[0]
    result['size'] = struct.unpack_from('<Q', prefix, offset=1)[0]
    result['revs'] = struct.unpack_from('>Q', prefix, offset=9)[0]

    if result['size'] != result['revs']:
        raise PrefixException("invalid prefix (checksum)")

    return result
