from pysondb import db
from Tests.Utils.pyson_db.builders.JobBuilder import Builder
from Tests.Utils.pyson_db.models.Engagements import Engagements

class EngagementsBuilder(Builder[Engagements]):
    """
    Builder class for creating and managing Engagements objects.
    This class is responsible for initializing an Engagements object with the provided data,
    building it, and saving it to the database.
    """
    def __init__(self, body: dict):
        """
        Initializes the EngagementsBuilder with the provided data.
        Args:
            body (dict): A dictionary containing the data to initialize the Engagements object.
            The dictionary should contain the necessary fields to create an Engagements object 
            - engagement_id
            - engagement_name
            - engagement_type
            - workspace_name
            - workspace_country_id
        """
        
        self.body = body
        self._engagements = Engagements(**body)

    def build(self) -> Engagements:
        """
        Builds and saves an Engagements object to the database.
        This method retrieves the database instance using the specified
        database location and name from the `_engagements` attribute.
        It then adds the `_engagements` object to the database and updates
        its `id` attribute with the newly generated ID.
        Returns:
            Engagements: The `_engagements` object with its `id` attribute updated.
        """

        engagement_db = db.getDb(f"{self._engagements.db_location}/{self._engagements.db_name}")
        self._engagements.id = engagement_db.add(self._engagements.to_dict())
        return self._engagements
