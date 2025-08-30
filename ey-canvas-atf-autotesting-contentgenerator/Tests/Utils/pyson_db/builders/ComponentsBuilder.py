from pysondb import db
from Tests.Utils.pyson_db.builders.JobBuilder import Builder
from Tests.Utils.pyson_db.models.Components import Components

class ComponentsBuilder(Builder[Components]):
    """
    Builder class for creating and managing Components objects.
    This class is responsible for initializing an Components object with the provided data,
    building it, and saving it to the database.
    """
    def __init__(self, body: dict):
        """
        Initializes the ComponentsBuilder with the provided data.
        Args:
            body (dict): A dictionary containing the data to initialize the Components object.
            The dictionary should contain the necessary fields to create an Components object 
            - components_link_requested
            - instructions_sent
        """
        
        self.body = body
        self._components = Components(**body)

    def build(self) -> Components:
        """
        Builds and saves an Components object to the database.
        This method retrieves the database instance using the specified
        database location and name from the `_components` attribute.
        It then adds the `_components` object to the database and updates
        its `id` attribute with the newly generated ID.
        Returns:
            Components: The `_components` object with its `id` attribute updated.
        """

        component_db = db.getDb(f"{self._components.db_location}/{self._components.db_name}")
        self._components.id = component_db.add(self._components.to_dict())
        return self._components
