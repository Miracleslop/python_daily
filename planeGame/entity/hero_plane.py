from planeGame.entity.entity import Entity
from commun.logger.Logger import log, Logger

lg = Logger('heroPlane')


class HeroPlane(Entity):
    __instance = None
    __first_init = True

    def __new__(cls, screen, imgPath):
        if not cls.__instance:
            cls.__instance = Entity.__new__(cls)
        return cls.__instance

    @log('creat HeroPlane', lg)
    def __init__(self, screen, imgPath):
        if self.__first_init:
            self.__name = 'hero'
            super().__init__(230, 700, screen, imgPath)
            self.__first_init = False

    def name(self):
        return self.__name
