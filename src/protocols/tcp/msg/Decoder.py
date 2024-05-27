
from conf.logconfig import logger
import traceback
from abc import ABC, abstractmethod

class Decoder(ABC):

    @abstractmethod
    def concyctencyCheck(self, msgBytes):
        pass
