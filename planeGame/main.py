# coding=utf-8
import pygame
from logger.Logger import Logger
from logger.Logger import log
from pygame.locals import *
from planeGame.entity.hero_plane import HeroPlane
from planeGame.key_control import KeyControl
import time

lg = Logger('main')

root_path = '/home/l/PycharmProjects/daily-strutil/'

"""
    1. creat view, show windows and background img
"""


@log('creat view, show windows and background img', lg)
def main():
    # 创建⼀个窗⼝，⽤来显示内容
    screen = pygame.display.set_mode((480, 852), 0, 32)

    # 创建⼀个和窗⼝⼤⼩的图⽚，⽤来充当背景
    background = pygame.image.load(root_path + 'planeGame/img/background.png')

    # 测试，⽤来创建⼀个玩家⻜机的图⽚
    hero = HeroPlane(screen, root_path + 'planeGame/img/hero1.png')
    try:
        while True:
            # pygame.event.clear()
            screen.blit(background, (0, 0))

            # 设定需要显示的⻜机图⽚
            hero.display()
            # listen key operation
            # print(pygame.event.get())
            if KeyControl.listen_key(hero):
                break

            pygame.display.update()
            time.sleep(1)
    except KeyboardInterrupt:
        lg.debug('game is terminated by keyboardInterrupt')


if __name__ == "__main__":
    main()
