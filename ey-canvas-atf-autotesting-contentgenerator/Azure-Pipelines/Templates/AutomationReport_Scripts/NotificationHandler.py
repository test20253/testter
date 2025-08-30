from abc import ABC, abstractmethod


class PostNotification(ABC):

    @abstractmethod
    def send_post_request(self, url: str, *args) -> dict:
        pass
