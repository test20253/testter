from pysondb import db
from Tests.Utils.pyson_db.builders.JobBuilder import Builder
from Tests.Utils.pyson_db.models.PocUsers import PocUsers

class PocUsersBuilder(Builder[PocUsers]):
    """
    Builder class for creating and managing POC User objects.
    This class is responsible for initializing a PocUsers object with the provided data,
    building it, and saving it to the database.
    """
    def __init__(self, body: dict):
        """
        Initializes the PocUsersBuilder with the provided data.
        Args:
            body (dict): A dictionary containing the data to initialize the PocUsers object.
            The dictionary should contain the necessary fields to create a PocUsers object
            - poc_user_name_token
            - instructions_sent
        """
        
        self.body = body
        self._pocusers = PocUsers(**body)

    def build(self) -> PocUsers:
        """
        Builds and saves a PocUsers object to the database.
        This method retrieves the database instance using the specified
        database location and name from the `_pocusers` attribute.
        It then adds the `_pocusers` object to the database and updates
        its `id` attribute with the newly generated ID.
        Returns:
            PocUsers: The `_pocusers` object with its `id` attribute updated.
        """

        pocusers_db = db.getDb(f"{self._pocusers.db_location}/{self._pocusers.db_name}")
        self._pocusers.id = pocusers_db.add(self._pocusers.to_dict())
        return self._pocusers
