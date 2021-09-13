from abc import ABC, abstractmethod


class BaseRestreamer(ABC):

    @abstractmethod
    def play(self): pass
