# from planeGame.entity.entity import Entity
from commun.logger.Logger import Logger
import pygame
from pygame.locals import *

lg = Logger('keyControl')


class KeyControl(object):

    def __new__(cls, *args, **kwargs):
        return None

    def __init__(self, entity):
        self.__entity = entity

    @staticmethod
    def listen_key(entity):
        is_exit = False
        for event in pygame.event.get([KEYDOWN, QUIT]):
            if event.type == QUIT:
                lg.debug('game exit!')
                is_exit = True
                break
            elif event.type == KEYDOWN:
                if event.key == K_a or event.key == K_LEFT:
                    lg.debug('operate left key')
                    entity.move_left()
                elif event.key == K_d or event.key == K_RIGHT:
                    lg.debug('operate right key')
                    entity.move_right()
                elif event.key == K_w or event.key == K_UP:
                    lg.debug('operate up key')
                    entity.move_up()
                elif event.key == K_s or event.key == K_DOWN:
                    lg.debug('operate down key')
                    entity.move_down()
                elif event.key == K_SPACE:
                    lg.debug('operate space key')
                    entity.attack()
        return is_exit
