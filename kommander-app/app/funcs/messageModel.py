import json

class MessageModel(object):
    """
    MessageModel class to represent a message
    """
    def __init__(self, details: str = None, parameters: dict = None):
        """
        Initialize MessageModel object

        Parameters:
            type: str
            thread: str
            details: str
            status: str
        """
        self.details = details
        self.parameters = parameters
        
    def __str__(self):
        debug = {}
        for attr_name in [attr for attr in dir(self) if not attr.startswith('__')]:
            if attr_name != "parameters":
                attr_value = getattr(self, attr_name)
                if attr_value is not None:
                    debug[attr_name] = attr_value
        
        message = {}

        message["debug"] = debug
        
        if self.parameters is not None:
            for attr, value in self.parameters.items():
                message[attr] = value

        return json.dumps(message)