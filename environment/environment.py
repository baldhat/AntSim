import myutils
from actors.Actor import Actor
from actors.FoodGatherer import FoodGatherer
import math
from random import *
from concurrent.futures import ThreadPoolExecutor
import numpy as np

from environment.FoodZone import FoodZone
from environment.ItemPos import ItemPos


class Environment:
    def __init__(self, size):
        self.actors = []
        self.food_zones = []
        self.food_indices = set()
        self.size = self.width, self.height = size
        self.movement_cost_factor = 0.1

    def on_init(self):
        self.actors = self.create_random_food_gatherers(num=200,
                                                        speed_range=(1, 5),
                                                        energy_range=(50, 200))
        self.food_zones = self.create_random_food_zones(60,
                                                        fertility_range=(1e-4, 1e-3),
                                                        x_range=(5, 15),
                                                        y_range=(5, 15))


    def step(self):
        executor = ThreadPoolExecutor(10)
        futures = []
        for food_zone in self.food_zones:
            for (x, y) in food_zone.spawn_food():
                self.food_indices.add(ItemPos(x + food_zone.pos[0], y + food_zone.pos[1]))

        for actor in self.actors:
            futures.append(executor.submit(actor.act, (self)))

        executor.shutdown(wait=True)

        for i, future in enumerate(futures):
            (orientation, dist) = future.result()
            self.move_actor(orientation, dist, self.actors[i])
            self.eat_near_food(self.actors[i])

        self.remove_all_dead_actors()

    def eat_near_food(self, actor):
        nearest_food_zone = None
        nearest_food_zone_dist = float('inf')
        for food_zone in self.food_zones:
            dist = myutils.dist(food_zone.mean_pos, actor.pos)
            if dist < nearest_food_zone_dist:
                nearest_food_zone = food_zone
                nearest_food_zone_dist = dist
        if nearest_food_zone_dist > max(nearest_food_zone.size) + 1:
            return
        rel_food_remove_list = []
        if len(nearest_food_zone.food_indices) > 0:
            for food_index in nearest_food_zone.food_indices:
                if myutils.dist(actor.pos, (nearest_food_zone.pos[0] + food_index[0],
                                            nearest_food_zone.pos[1] + food_index[1])) < 1:
                    actor.energy += 10
                    rel_food_remove_list.append(food_index)

            for food_index in rel_food_remove_list:
                abs_index = (food_index[0] + nearest_food_zone.pos[0], food_index[1] + nearest_food_zone.pos[1])
                self.food_indices.discard(ItemPos(abs_index[0], abs_index[1]))
                mask = np.zeros((nearest_food_zone.size[1], nearest_food_zone.size[0]))
                mask[food_index[1], food_index[0]] = 1.
                nearest_food_zone.grid = np.logical_xor(nearest_food_zone.grid, mask)


    def add(self, actor: Actor):
        self.actors.append(actor)

    def move_actor(self, orientation, distance, actor):
        # TODO: Check if out of env
        x_move, y_move = (math.cos(orientation) * distance, math.sin(orientation) * distance)
        needed_energy = distance * actor.speed * self.movement_cost_factor  # Energy consumption ~ speed²
        if actor.energy >= needed_energy:
            actor.pos = (actor.pos[0] + x_move, actor.pos[1] + y_move)
            actor.energy -= needed_energy
        else:   # Wenn nicht genügend Energie übrig ist, gehe so weit wie noch möglich
            actor.pos = (actor.x + (x_move * (actor.energy / needed_energy)),
                         actor.y + (y_move * (actor.energy / needed_energy)))
            actor.energy = 0

    def remove_all_dead_actors(self):
        for actor in self.actors:
            if actor.energy == 0:
                self.actors.remove(actor)
            else:
                actor.num_iters_survived += 1

    def get_nearest_actor(self, pos):
        smallest_dist = float("inf")
        nearest = self.actors[0]
        for actor in self.actors:
            dist = myutils.dist(actor.pos, pos)
            if dist < smallest_dist:
                nearest = actor
                smallest_dist = dist
        return nearest

    def create_random_food_gatherers(self, num, speed_range, energy_range):
        gatherers = []
        for i in range(num):
            gatherers.append(FoodGatherer(pos=(randrange(0, self.width), randrange(0, self.height)),
                                          speed=random() * (speed_range[1] - speed_range[0]) + speed_range[0],
                                          energy=randrange(energy_range[0], energy_range[1])))
        return gatherers

    def create_random_food_zones(self, num, fertility_range, x_range, y_range):
        zones = []
        for i in range(num):
            zones.append(FoodZone(pos=(randrange(0, self.width), randrange(0, self.height)),
                                  fertility=random() * (fertility_range[1] - fertility_range[0]) + fertility_range[0],
                                  size=(randrange(x_range[0], x_range[1]), randrange(y_range[0], y_range[1]))))
        return zones
