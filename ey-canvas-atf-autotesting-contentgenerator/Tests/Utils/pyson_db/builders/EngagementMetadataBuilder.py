from pysondb import db
from enum import Enum
from Tests.Utils.pyson_db.models.EngagementMetadata import EngagementMetadata
from Tests.Utils.pyson_db.builders.JobBuilder import Builder




class EngagementMetadataBuilder(Builder[EngagementMetadata]):
    """
    This class creates new Jobs, all the attributes can be override if needed using the with methods.
    """

    def __init__(self):
        self._engagement_metadata = EngagementMetadata()

    def with_db_location(self, db_location: str):
        self._engagement_metadata.db_location = db_location
        return self

    def build(self) -> EngagementMetadata:
        """
        Returns:Build a Job with the jobBuilder attributes

        """
        engagement_metadata_db = db.getDb(f"{self._engagement_metadata.db_location}/{self._engagement_metadata.db_name}")
        dict_representation = self._engagement_metadata.to_dict()
        dict_representation = {k: (v.value if isinstance(v, Enum) else v) for k, v in dict_representation.items()}
        self._engagement_metadata.id = engagement_metadata_db.add(dict_representation)
        return self._engagement_metadata
