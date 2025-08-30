from Tests.Utils.pyson_db.PysonDbModelBase import PysonDbModelBase

class Engagements(PysonDbModelBase):
    
    """
    Model for Engagements schema that will be used in pysondb
    """
    def __init__(self, engagement_id: str, engagement_name: str, engagement_type: str, workspace_name: str, workspace_country_id:str):
        """
        Initializes an instance of the Engagements model.
        Args:
            engagement_id (str): The unique identifier for the engagement.
            engagement_name (str): The name of the engagement.
            engagement_type (str): The type/category of the engagement.
            workspace_name (str): The name of the associated workspace.
            workspace_country_id (str): The country identifier for the workspace.
        """
        
        PysonDbModelBase.__init__(self)
        self.engagement_id = engagement_id
        self.engagement_name = engagement_name
        self.engagement_type = engagement_type
        self.workspace_name = workspace_name
        self.workspace_country_id = workspace_country_id