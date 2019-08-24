class AiotasksException(Exception):
    pass

class UnknownBackend(AiotasksException):
    pass

class ErrorConnectBackend(AiotasksException):
    pass

class LTaskNotStarted(AiotasksException):
    pass

class LTaskNotFount(AiotasksException):
    pass
