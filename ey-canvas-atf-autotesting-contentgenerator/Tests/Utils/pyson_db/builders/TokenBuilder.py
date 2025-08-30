from datetime import datetime
from pysondb import db
from Tests.Utils.pyson_db.models.Job import Status, Job
from typing import TypeVar, Generic
from abc import ABC, abstractmethod
from Tests.Utils.pyson_db.builders.JobBuilder import Builder
from Tests.Utils.pyson_db.models.Token import Token

T = TypeVar('T')


class TokenBuilder(Builder[Token]):
    """
    This class creates new Jobs, all the attributes can be override if needed using the with methods.
    """

    def __init__(self):
        self._token = Token()

    def with_db_location(self, db_location: str):
        self._token.db_location = db_location
        return self

    def build(self) -> Token:
        """
        Returns:Build a Job with the jobBuilder attributes

        """
        token_db = db.getDb(f"{self._token.db_location}/{self._token.db_name}")
        self._token.id = token_db.add(self._token.to_dict())
        return self._token