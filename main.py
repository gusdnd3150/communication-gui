
import sys
sys.path.append('.')
from src.init import InitClass
from conf.logconfig import logger
# 메인 프로세스 실행
if __name__ == '__main__':
    logger.info('start application')
    InitClass() # 메인 클래스


