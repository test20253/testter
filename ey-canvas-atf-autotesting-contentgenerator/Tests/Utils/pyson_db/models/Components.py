from Tests.Utils.pyson_db.PysonDbModelBase import PysonDbModelBase

class Components(PysonDbModelBase):
    
    """
    Model for Components schema that will be used in pysondb
    """
    def __init__(self, components_link_requested: list = None, instructions_sent: list = None):
        """
        Initializes a new instance of the Components DB.
        Args:
            components_link_requested (list, optional): A list of requested component links. Defaults to None.
            instructions_sent (list, optional): A list of instructions that have been sent. Defaults to None.
        """
        
        PysonDbModelBase.__init__(self)
        self.components_link_requested = components_link_requested
        self.instructions_sent = instructions_sent