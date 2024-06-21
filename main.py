
import sys
sys.path.append('.')
# from src.utils.Container import Container
from src.init import InitClass
from conf.InitData_n import *

# 메인 프로세스 실행
if __name__ == '__main__':
    print('start application')
    # ct = Container()
    # ct.appIni_bean()

    InitClass() # 메인 클래스


