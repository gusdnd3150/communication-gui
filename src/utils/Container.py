

from conf.logconfig import logger
from abc import abstractmethod, ABC
from dependency_injector import containers, providers
from src.utils.InitData import InitData

# Bean 설정 클래스
class Container(containers.DeclarativeContainer):

    logger.info('Container start')
    # InitData_bean = providers.Singleton(InitData)



