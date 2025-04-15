
from conf.logconfig import logger
from src.protocols.SendHandler import SendHandler
# from conf.skModule import runChannels
import conf.skModule as modules
import gc
import objgraph


class SchController():

    # guide
    # 데이터 전송 방법
    # skLogger = reciveObj['LOGGER']
    # Channel = reciveObj['CHANNEL']
    # thread = reciveObj['THREAD']
    # 1. SendHandler.sendSkId(skId, msgId, data)
    # 2. thread.sendBytesToChannel(channel, '00200105000000000000'.encode('utf-8'))
    # 3. thread.sendMsgToChannel(channel, map) // map 안    MSG_ID    키: 값이    있어야함

    sendHandler = None
    def __init__(self):
        logger.info('init schController')
        self.sendHandler = SendHandler()

    def test(self, reciveObj):
        skLogger = reciveObj['LOGGER']
        returnJson = {}
        try:
            # objgraph.show_most_common_types(limit=20)
            skLogger.info(f' 스케줄 테스트 ')

            client_threads = self.get_instances_by_class_name("ClientThread")
            print(f"Found {len(client_threads)} ClientThread instances")

            client_threads = self.get_instances_by_class_name("ServerThread")
            print(f"Found {len(client_threads)} ServerThread instances")

            client_threads = self.get_instances_by_class_name("ThreadPoolExecutor")
            print(f"Found {len(client_threads)} ThreadPoolExecutor instances")

            client_threads = self.get_instances_by_class_name("BzActivator2")
            print(f"Found {len(client_threads)} BzActivator2 instances")

            client_threads = self.get_instances_by_class_name("BzSchedule2")
            print(f"Found {len(client_threads)} BzSchedule2 instances")

            print(f"Found {len(modules.runChannels)} runChannels cnt")

            # self.sendHandler.sendSkId('SSSSS', 'PLC_WRITE', returnJson)
        except Exception as e:
            skLogger.error(f'SchController.test() Exception :: {e}')


    def get_instances_by_class_name(self,class_name: str):
        return [obj for obj in gc.get_objects() if type(obj).__name__ == class_name]