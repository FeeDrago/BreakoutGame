import pygame
from constants import *


class Block(pygame.Rect):

    def __init__(self, left, top, width, height, color):
        super().__init__(left, top, width, height)
        self.color = color

    def __repr__(self) -> str:
        return super().__repr__() 
    