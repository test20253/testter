import threading
from robot.utils.asserts import fail
from typing import Dict, Optional
from datetime import datetime, timedelta

class TokensUsers:
    _instance: Optional['TokensUsers'] = None
    _lock = threading.Lock()
    _data: Dict[str, Dict[str, str]] = {}
    _token_duration: int = 3000

    def __init__(self, user_name: str, token_name: str, token_value: str):
        self._initialize(user_name, token_name, token_value)

    def _initialize(self, user_name: str, token_name: str, token_value: str):
        print(f'[INFO] Instance Creation!')
        try:
            self._data[user_name] = {
                token_name: token_value,
                "creation_time": datetime.now()
            }
        except KeyError:
            fail(f'It was not possible to initialize the information of the engagement: {user_name}')

    @classmethod
    def _initialize_if_needed(cls, user_name: str, token_name: str, token_value: str):
        
        if user_name not in cls._data:
            cls._instance._initialize(user_name, token_name, token_value)
        elif token_name not in cls._data[user_name]:
            print(f'[INFO] token {token_name} Updated for user: {user_name}')
            cls._data[user_name][token_name] = token_value

    @classmethod
    def get_instance(cls, user_name: str, token_name: str, token_value: str = None) -> 'TokensUsers':
        if (not any(token_name in dic.get(user_name, {}) for dic in cls._data.values()) and None != token_value):
            with cls._lock:
                if not cls._instance:
                    cls._instance = TokensUsers(user_name, token_name, token_value)
                cls._initialize_if_needed(user_name, token_name, token_value)
        return cls._instance


    @staticmethod
    def set_token(user_name: str, token_name: str, token_value: str):
        tokens_users = TokensUsers.get_instance(user_name, token_name, token_value)
        tokens_users._update_expired_token(user_name, token_name, token_value)

    @staticmethod
    def get_token(user_name: str, token_name: str) -> str:
        tokens_users = TokensUsers.get_instance(user_name, token_name)
        return tokens_users._data[user_name][token_name]

    def _update_expired_token(self, user_name: str, token_name: str, token_value: str):
        token_data = self._data[user_name]
        creation_time = token_data['creation_time']
        current_time = datetime.now()
        token_duration = timedelta(seconds=self._token_duration)
        print(f'[INFO] Token {token_name} for use: {user_name} creation time: {creation_time} ')
        print(f'[INFO] Time {current_time - creation_time} token duration: {token_duration} result: {(current_time - creation_time) > token_duration} ')
        if (current_time - creation_time) > token_duration:
            print(f'[INFO] Token {token_name} has expired for user: {user_name}')
            self._initialize(user_name=user_name, token_name=token_name, token_value=token_value)