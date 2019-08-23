class AiotasksException(Exception):
    pass

class ErrorConnectBackend(AiotasksException):
    pass

class LTaskNotStarted(AiotasksException):
    pass

class LTaskNotFount(AiotasksException):
    pass
