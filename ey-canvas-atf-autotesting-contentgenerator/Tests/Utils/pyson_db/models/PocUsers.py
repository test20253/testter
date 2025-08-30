from Tests.Utils.pyson_db.PysonDbModelBase import PysonDbModelBase

class PocUsers(PysonDbModelBase):
    
    """
    Model for POC Users schema that will be used in pysondb
    """
    def __init__(self, poc_user_name_token: list = None):
        """
        Initializes a new instance of the POC Users DB.
        Args:
            poc_user_name_token (list, optional): A list of POC user name tokens. Defaults to None.
        """
        
        PysonDbModelBase.__init__(self)
        self.poc_user_name_token = poc_user_name_token