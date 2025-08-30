from Tests.Utils.logging.LoggerFactory import Logger

logger = Logger(__name__).get_logger()
from Tests.Utils.tokens.TokenNames import TokenNames
import inspect
from functools import wraps

from Tests.custom_methods.TokenMethodsV2 import TokenMethodsV2


def _get_parameter_from_kwargs_or_args(args, kwargs, parameter_index, parameter):
    """
    This method get the value of the parameter of a method and search for the value in kwargs or args
    Args:
        args: args from the function
        kwargs: kwargs from the function
        parameter_index: the number of position in args in which the parameter is
        parameter: the name of the parameter

    Returns:
        The value of the parameter
    """
    try:
        if parameter in kwargs:
            parameter_value = kwargs[parameter]
        else:
            parameter_value = args[parameter_index]

    except:
        parameter_value = None
    return parameter_value


def add_headers(token_name):
    def decorator(func):
        signature = inspect.signature(func)
        keys = list(signature.parameters.keys())

        @wraps(func)
        def wrapper(*args, **kwargs):
            user_name_token_index = keys.index('user_name_token')
            user_name_token = _get_parameter_from_kwargs_or_args(
                args=args, kwargs=kwargs,
                parameter_index=user_name_token_index,
                parameter="user_name_token"
            )
            token = TokenMethodsV2().get_token(token_name=token_name, user_name_token=user_name_token)
            auth_headers = {
                "Authorization": f"Bearer {token}",
                "User-Agent": "Canvas Automation"
            }

            # Handle headers safely
            if 'headers' in kwargs:
                # Merge with existing headers
                kwargs['headers'] = {**kwargs['headers'], **auth_headers}
            else:
                # Check if headers was passed positionally
                if 'headers' in keys:
                    headers_index = keys.index('headers')
                    if len(args) > headers_index:
                        args = list(args)
                        existing_headers = args[headers_index]
                        args[headers_index] = {**existing_headers, **auth_headers}
                        args = tuple(args)
                    else:
                        kwargs['headers'] = auth_headers
                else:
                    kwargs['headers'] = auth_headers

            return func(*args, **kwargs)

        return wrapper
    return decorator
