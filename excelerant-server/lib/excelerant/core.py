from abc import ABC, abstractmethod
from datetime import time
from pixtendv2s import PiXtendV2S

__author__ = "Eike Meyer"
__version__ = "0.1.0"


class ExcelerantCore(ABC):
    def __init__(self):
        self._pixtend = PiXtendV2S()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._pixtend.close()

    @abstractmethod
    def getFanPower(self):
        pass

    @abstractmethod
    def setFanPower(self):
        pass


def is_time_between(time: time, start: time, end: time) -> bool:
    if start <= end:
        return start <= time < end
    else:
        return start <= time or time < end
