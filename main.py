
import sys
sys.path.append('.')
from src.init import InitClass
from conf.logconfig import logger
import conf.skModule as module

# 메인 프로세스 실행
if __name__ == '__main__':
    logger.info('start application')
    InitClass() # 메인 클래스
    logger.info(f'system close')
    for i, sch in enumerate(module.sokcetSch):
        runThread = sch['SK_THREAD']
        if runThread.isRun:
            runThread.stop()

