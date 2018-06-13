from logger.Logger import Logger
import pygame

lg = Logger('entity')

lm_distance = 10
rm_distance = 10
um_distance = 10
dm_distance = 10


class Entity(object):
    def __init__(self, x, y, screen, imgPath):
        self.__x = x
        self.__y = y
        self.__screen = screen
        self.__img = pygame.image.load(imgPath)

    def display(self):
        self.__screen.blit(self.__img, (self.__x, self.__y))

    def move_left(self):
        self.__x -= lm_distance

    def move_right(self):
        self.__x += rm_distance

    def move_up(self):
        self.__y -= um_distance

    def move_down(self):
        self.__y += dm_distance

    def attack(self):
        pass
