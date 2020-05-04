
class Actor:
    def __init__(self, pos, color, energy, speed, orientation):
        self.pos = self.x, self.y = pos
        self.color = color
        self.energy = energy
        self.num_iters_survived = 0
        self.speed = speed
        self.orientation = orientation

    def act(self, environment):
        pass

    def __str__(self):
        return f"{self.__class__}:\n\tSpeed:\t{self.speed}"