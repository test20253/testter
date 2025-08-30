import datetime
from enum import Enum
from Tests.Utils.pyson_db.PysonDbModelBase import PysonDbModelBase


class Status(str, Enum):
    NEW: str = "NEW"
    IN_PROGRESS: str = "IN_PROGRESS"
    FINISHED: str = "FINISHED"


class Result(str, Enum):
    PASSED: str = "PASSED"
    FAILED: str = "FAILED"
    INITIAL: str = "INITIAL"


class Job(PysonDbModelBase):
    """
    Model for Job schema that will be used in pysondb
    """

    def __init__(self, timeout: int, creation_time: str = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")):
        PysonDbModelBase.__init__(self)
        self.output_message = ""
        self.creation_time = creation_time
        self.status = Status.NEW
        self.timeout = timeout
        self.result = Result.INITIAL
        self.log = ""
        self.id = 0

    def set_status(self, status: Status):
        self.status = status
        return self

    def set_output_message(self, output_message: str):
        self.output_message = output_message
        return self
