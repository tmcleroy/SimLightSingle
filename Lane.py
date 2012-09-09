class Lane:

    def __init__(self, id, rules):
        self.id = id
        self.vehicles = []
		
        self.rules = rules
        self.allowsStraight = "straight" in rules
        self.allowsRight =  "right" in rules
        self.allowsLeft = "left" in rules

    def getLastVehicle(self):
        if len(self.vehicles) > 0:
            return self.vehicles[len(self.vehicles)-1]
        else:
            return False
