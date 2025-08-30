from datetime import datetime, timedelta
from enum import Enum
from Tests.Utils.pyson_db.PysonDbModelBase import PysonDbModelBase




class Token(PysonDbModelBase):
    """
    Model for Job schema that will be used in pysondb
    """

    def __init__(self,):
        PysonDbModelBase.__init__(self)
        self.token = ""
        self.creation_time = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        self.expiration_time = (datetime.now() + timedelta(minutes = 40)).strftime("%m/%d/%Y, %H:%M:%S")
        self.last_status_code = ""
        self.location_url = ""
        self.resource_name = ""
        self.token_name = ""
        self.user = ""
        self.id = 0

    def get_token_db(self,db_name) -> str:
        """
        Method for save the current object to the pysondb
        Returns:updated record id
        """

        generic_db = self.get_or_create_db(db_name)

        return generic_db