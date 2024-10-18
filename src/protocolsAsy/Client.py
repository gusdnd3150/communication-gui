


from abc import *


class Client(metaclass=ABCMeta):

    @abstractmethod
    def sendBytesToChannel(self, channel ,bytes):
        pass

    @abstractmethod
    def sendBytesToAllChannels(self, bytes):
        pass

    @abstractmethod
    def sendMsgToChannel(self, channel, obj):
        pass

    @abstractmethod
    def sendMsgToAllChannels(self, obj):
        pass

