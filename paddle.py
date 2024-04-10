import pygame
from constants import *


class Paddle(pygame.Rect):
    def __init__(self, left, top, width, height, color):
        super().__init__(left, top, width, height)
        self.color = color