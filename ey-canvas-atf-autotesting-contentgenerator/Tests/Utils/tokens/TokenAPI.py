from Tests.Utils.pyson_db.builders.TokenBuilder import TokenBuilder
from Tests.Utils.pyson_db.models.Token import Token
from Tests.Utils.logging.LoggerFactory import Logger
logger = Logger(__name__).get_logger()

class TokenAPI(Token):
    def __init__(self, ):
        Token.__init__(self)
        self.token_db_name = "Token"

    def get_token(self, body):
        """
        Get an entry in the pysondb for the given body
        Args:
            body: dictionary with the following keys
                  user
                  token_name
                  location_url
        Returns:
                None
        """
        logger.debug(f"Trying to get token with the following information {body}")
        if not body["location_url"]:
            body["location_url"] = None
        db = self.get_token_db(self.token_db_name)
        try:
            token_db_obj = \
                db.getByQuery({"user": body["user"], "location_url": body["location_url"]})
        except Exception as e:
            logger.error(f"Error trying to get the token from the pysonDb, make sure proper body was sent: {str(e)}")
            raise e
        if not token_db_obj:
            return None
        return token_db_obj[0]

    def post_token(self, body):
        """
        Insert an entry in the pysondb for the given token
        Args:
            body: dictionary with the following keys
                  location_url
                  resource_name
                  token_name
                  user
                  token
        Returns:
            None
        """
        logger.debug(f"Trying to insert the just obtained MSAL token to the pysonDb")
        token_obj = TokenBuilder().build()
        try:
            token_obj.location_url = body["location_url"]
            token_obj.token_name = body["token_name"]
            token_obj.user = body["user"]
            token_obj.token = body["token"]
            token_obj.resource_name = body["resource_name"]
        except Exception as e:
            logger.error(f"Make sure the body was properly sent as per of the TokenAPI.post_token documentation {str(e)}")
        token_obj.update_db()
        logger.info(f"Token inserted to the pysonDb")

    def put_token(self, body):
        """
        Update entry in the pysondb for the given token
        Args:
            body:dictionary with the following keys
                  user
                  token_name
                  location_url
                  token
        Returns:
                None
        """
        logger.debug(f"getting token to update using the following data: {body}")
        db = self.get_token_db(self.token_db_name)

        token_db_obj = db.getByQuery({"token_name": body["token_name"],"user": body["user"], "location_url": body["location_url"]})[0]
        try:
            token_db_obj["token"] = body["token"]
            token_db_obj["creation_time"] = body["creation_time"]
            token_db_obj["expiration_time"] = body["expiration_time"]
            db.updateById(token_db_obj["id"], token_db_obj)
        except Exception as e:
            logger.error(
                f"Make sure the body was properly sent as per of the TokenAPI.put_token documentation, or verify if the token send is actually present in the pyson db {str(e)}")
            raise e
        logger.info(f"Token updated in the pysonDb")
