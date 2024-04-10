import pygame
from constants import *


class Ball:
    def __init__(self, center: tuple, radius:int=BALL_RAD, color:tuple=WHITE, width=0,vel_incr:int=0 ):
        self.center = center
        self.radius = radius
        self.color = color
        self.width = width
        self.vel = vel_incr + BALL_VEL