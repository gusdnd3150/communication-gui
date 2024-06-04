

from conf.logconfig import logger
from dependency_injector import containers, providers

from src.protocols.SendHandler import SendHandler

# Bean 설정 클래스
class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    service_a = providers.Singleton(SendHandler)

    logger.info('Container start')
    # InitData_bean = providers.Singleton(InitData)



