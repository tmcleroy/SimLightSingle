class Road:

    def __init__(self, id, l1, l2):
        self.id = id
        self.lane1 = l1
        self.lane2 = l2

    def getNumVehicles(self):
        return len(self.lane1.vehicles+self.lane2.vehicles)

    def isOdd(self):
        return self.id%2

    def isEven(self):
        return not self.isOdd()
