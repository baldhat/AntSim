import myutils
from actors.Actor import Actor
import math
from random import *
import time


class FoodGatherer(Actor):
    def __init__(self, pos, color=(0, 0, 0), energy=100, speed=1, orientation=0):
        super().__init__(pos, color, energy, speed, orientation)

    def act(self, environment):
        food_pos, dist = self.get_nearest_food_position(environment)
        if dist == float("inf"):
            self.orientation = self.orientation + (random() * math.pi / 8) - (math.pi / 16)
            distance = self.speed * random()
        else:
            self.orientation = math.atan2(self.pos[1] - food_pos[1], self.pos[0] - food_pos[0]) + math.pi
            if dist < self.speed:
                distance = dist
            else:
                distance = self.speed
        return self.orientation, distance

    def get_nearest_food_position(self, environment):
        # TODO: Check for nearest food_zone first, is more efficient
        smallest_dist = float("inf")
        smallest = None
        for food_index in environment.food_indices:
            dist = myutils.dist(food_index, self.pos)
            if dist < smallest_dist:
                smallest = food_index
                smallest_dist = dist
        return smallest, smallest_dist
