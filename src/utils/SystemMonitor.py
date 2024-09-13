

from conf.logconfig import logger
import threading

class SystemMonitor(threading.Thread):


    mainInstance =None

    def __init__(self, mainInstance):
        self.mainInstance = mainInstance
        super().__init__()


    def run(self):
        try:
            pass
            # logger.info('system Monitoring Start')
            #
            # # 현재 실행 중인 프로세스의 프로세스 ID를 가져옵니다.
            # pid = psutil.Process().pid
            #
            # # 현재 실행 중인 프로세스 객체를 생성합니다.
            # process = psutil.Process(pid)
            # while True:
            #                    # cpu 사용률 출력
            #     cpu_usage = process.cpu_percent()
            #     self.mainInstance.bar_cpu_stat.setValue(int(cpu_usage))
            #     # 1초 간격으로 스레드 수를 가져옵니다.
            #     time.sleep(1)
        except Exception as e:
            logger.info(f' Monitoring exception : {e}')

