

from conf.logconfig import logger
from abc import abstractmethod, ABC
from dependency_injector import containers, providers
from src.utils.InitData import InitData

# Bean 설정 클래스
class Container(containers.DeclarativeContainer):

    InitData_bean = providers.Factory(InitData)
    # car_factory = providers.Factory(Car,tier=common_tier_factory)