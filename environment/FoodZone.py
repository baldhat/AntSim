import numpy as np

"""
A zone in which food can spawn
"""


class FoodZone:
    def __init__(self, pos, size=(10, 12), fertility=1e-4):
        """Parameters:
        :type size: (int, int)
        :parameter size: The radius of the zone

        :type fertility: double
        :parameter fertility: probability of a food item spawning on 1px²

        :type pos: (int, int)
        :parameter pos: position of the zone in the environment

        Total amount of food spawning each tick: Pi * radius * radius * fertility = Area * fertility
        """
        self.size = size
        self.fertility = fertility
        self.pos = pos
        self.grid = np.zeros((self.size[1], self.size[0]))
        self.mean_pos = (pos[0] + size[0] / 2, pos[1] + size[1] / 2)
        self.food_indices = []

    def spawn_food(self):
        arr = np.random.binomial(1, self.fertility, size=(self.size[1], self.size[0]))
        ind = np.unravel_index(np.argwhere(arr == 1), (self.size[1], self.size[0]))
        self.grid = np.logical_or(self.grid, arr)
        grid_indices = np.unravel_index(np.argwhere(self.grid == 1), (self.size[1], self.size[0]))
        self.food_indices = np.flip(grid_indices[1]).tolist()
        ret = np.flip(ind[1])
        return ret.tolist()

    def __str__(self):
        return f"FoodZone:\n\tSize: {self.size}\n\tFertility: {self.fertility}"