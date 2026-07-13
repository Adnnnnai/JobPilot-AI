from abc import ABC
from abc import abstractmethod


class BaseTool(ABC):

    name = ""

    description = ""

    @abstractmethod
    def run(self, *args, **kwargs):
        pass
