from pysondb import db
import pathlib

from pysondb.db import JsonDatabase


class PysonDbModelBase(object):
    """
    Base class for models that want to make use of pysondb features
    """
    def __init__(self) -> None:
        self.db_name = f"{self.__class__.__name__}.json"
        self.db_location: str = "Tests/resources/local_db"

    def to_dict(self):
        """
        Method for serialize the model to a dict, for future save in pysondb
        Returns: current object converted to dictionary
        """
        self_to_dict = self.__dict__
        return self_to_dict

    def update_db(self, body = None) -> str:
        """
        Updates the database record associated with the current instance.
        Args:
            body (dict, optional): A dictionary containing the updated data for the record. 
                If not provided, the instance's current data (converted to a dictionary) 
                will be used.
        Returns:
            str: The ID of the updated record.
        """
        generic_db = db.getDb(f"{self.db_location}/{self.db_name}")
        if body is None:
            generic_db.updateById(self.id, self.to_dict())
        else:
            generic_db.updateById(self.id, body)
        return self.id

    def get_or_create_db(self, db_name:str = None) -> JsonDatabase:
        """
        Retrieves an existing JSON database or creates a new one if it does not exist.
        Args:
            db_name (str, optional): The name of the database file (without extension) 
                to retrieve or create. If not provided, the default database name 
                (`self.db_name`) will be used.
        Returns:
            JsonDatabase: An instance of the JSON database.
        """
        pathlib.Path(self.db_location).mkdir(parents=True, exist_ok=True)
        if db_name:
            generic_db = db.getDb(f"{self.db_location}/{db_name}.json")
        else:
            generic_db = db.getDb(f"{self.db_location}/{self.db_name}")

        return generic_db