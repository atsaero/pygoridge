class GoridgeException(Exception):
    pass


class InvalidArgumentException(GoridgeException):
    pass


class PrefixException(GoridgeException):
    pass


class TransportException(GoridgeException):
    pass


class RelayException(GoridgeException):
    pass


class ServiceException(GoridgeException):
    pass


class RelayFactoryException(GoridgeException):
    pass


class RoadRunnerException(Exception):
    pass


class WorkerException(RoadRunnerException):
    pass
