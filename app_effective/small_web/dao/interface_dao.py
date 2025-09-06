from abc import ABC, abstractmethod


class AbstractDAO(ABC):
    # Data Access Object

    @abstractmethod
    def get_permissions(self):
        raise NotImplementedError

    @abstractmethod
    def get_sample(self, permission, mark):
        raise NotImplementedError

    @abstractmethod
    def post_sample(self, permission):
        raise NotImplementedError
