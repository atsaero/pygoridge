PREFIX_LENGTH = 17


class PayloadType:
    PAYLOAD_NONE    = 2
    PAYLOAD_RAW     = 4
    PAYLOAD_ERROR   = 8
    PAYLOAD_CONTROL = 16


WORKER_STOP_MESSAGE = {"stop": True}
