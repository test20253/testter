from enum import Enum
from typing import Dict

from Tests.Utils.pyson_db.PysonDbModelBase import PysonDbModelBase

class EngagementType(str, Enum):
    ROLL_FORWARD_ENGAGEMENT = "RF_Engagement"
    COPY_ENGAGEMENT = "Copy_Engagement"
    RESTORE_ENGAGEMENT = "RS_Engagement"
    DEFAULT_ENGAGEMENT = "Default_Engagement"
    PRIMARY_ENGAGEMENT = "Primary_Engagement"

class InfoType(str, Enum):
    ACCOUNT = "Account"
    SCOT = "Scot"
    DEFAULT_INFO = "Default_Info"
    GROUP_COMPONENT = "Group_Component"
    DOCUMENT = "Document"
    USER = "User"
    CLIENT_REQUEST = "Client_Request"
    ENGAGEMENT = "Engagement"
    PROFILE = "Profile"
    ANNOTATION = "Annotation"
    ITCONTROL = "ITControl"
    ITAPPLICATION = "ITApplication"

class EngagementMetadata(PysonDbModelBase):
    """
    Model for Engagement Metadata schema that will be used in pysondb
    """


    def __init__(self):
        PysonDbModelBase.__init__(self)
        self.engagement_id = ""
        self.engagement_type = EngagementType.DEFAULT_ENGAGEMENT
        self.info_type = InfoType.DEFAULT_INFO
        self.json_details = {}
        self.id = 0

    def get_engagement_metadata_db(self, db_name) -> str:
        """
        Method for save the current object to the pysondb
        Returns:updated record id
        """
        generic_db = self.get_or_create_db(db_name)
        return generic_db

    def create_query(self, engagement_id: int, eng_type: EngagementType= None, info_type: InfoType=None) -> Dict[str, any]:
        """
        Creates a query to retrieve metadata based on engagement_id, engagement_type, and info_type.
        Args:
            engagement_id (int): ID of the engagement.
            eng_type (EngagementType, optional): The type of engagement.
            info_type (InfoType, optional): The type of information.
        Returns:
            dict: A dictionary representing the query.
        """
        query = {"engagement_id": engagement_id}
        if eng_type:
            query["engagement_type"] = eng_type.value
        if info_type:
            query["info_type"] = info_type.value
        return query

