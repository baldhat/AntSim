

class ItemPos:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y

    def __hash__(self):
        return int(str(self.x)+str(self.y))

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()
