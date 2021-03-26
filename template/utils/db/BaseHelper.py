from abc import ABCMeta, abstractmethod


class BaseHelper(metaclass=ABCMeta):
    @abstractmethod
    async def connect(self):
        pass