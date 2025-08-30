from datetime import datetime
from pysondb import db
from Tests.Utils.pyson_db.models.Job import Status, Job
from typing import TypeVar, Generic
from abc import ABC, abstractmethod

T = TypeVar('T')


class Builder(ABC, Generic[T]):
    """
    Builder abstract class to make the builders to implement the build command
    """
    @abstractmethod
    def build(self) -> T:
        pass


class JobBuilder(Builder[Job]):
    """
    This class creates new Jobs, all the attributes can be override if needed using the with methods.
    """

    def __init__(self, timeout: int):
        self.output_message = ""
        self.status = Status.NEW
        self.timeout = timeout
        self._job = Job(timeout)

    def with_db_location(self, db_location: str):
        self._job.db_location = db_location
        return self

    def with_creation_time(self, creation_time: str):
        self._job.creation_time = creation_time
        return self

    def build(self) -> Job:
        """
        Returns:Build a Job with the jobBuilder attributes

        """
        job_db = db.getDb(f"{self._job.db_location}/{self._job.db_name}")
        self._job.id = job_db.add(self._job.to_dict())
        return self._job
