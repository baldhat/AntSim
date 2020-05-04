from actors.Actor import Actor
from random import randrange
from random import random
import math


class RandomActor(Actor):
    def __init__(self, pos, color=(0, 0, 0), energy=100, speed=1, orientation=0):
        super().__init__(pos, color, energy, speed, orientation)

    def act(self, environment):
        self.orientation = self.orientation + (random() * math.pi / 8) - (math.pi / 16)
        distance = self.speed * random()
        return self.orientation, distance
