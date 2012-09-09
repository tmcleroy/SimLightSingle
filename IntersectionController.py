import time


class IntersectionController:

    def __init__(self, p1, p2, p3, p4, r1, r2, r3 ,r4):
        self.pole1 = p1
        self.pole2 = p2
        self.pole3 = p3
        self.pole4 = p4
        self.poles = [self.pole1, self.pole2, self.pole3, self.pole4]

        self.road1 = r1
        self.road2 = r2
        self.road3 = r3
        self.road4 = r4
        self.roads = [self.road1, self.road2, self.road3, self.road4]

        self.oddPoles = [self.poles[0], self.poles[2]]
        self.evenPoles = [self.poles[1], self.poles[3]]

        self.prev = self.getMostPopulatedRoad()
        self.prevfc = 0
        


    def auto(self, fc, mode):
        if mode == "mostPopulated":
            #if the most populated road changes from even to odd, set the frame count
            if not (self.getMostPopulatedRoad().isEven() == self.prev.isEven()): self.prevfc = fc
            if self.getMostPopulatedRoad().isEven():
                self.evenStraightFlow(fc)
            else:
                self.oddStraightFlow(fc)
            self.prev = self.getMostPopulatedRoad()
            
            

    def getMostPopulatedRoad(self):
        #default
        max = self.road1
        for road in self.roads:
            if road.getNumVehicles() > max.getNumVehicles(): max = road
        return max


    def oddStraightFlow(self, fc):
        if fc - self.prevfc < 360:
            for pole in self.poles:
                if pole.light1.state == "go": pole.light1.setState("slow")
                if pole.light2.state == "go": pole.light2.setState("slow")
        else:   
            for pole in self.oddPoles:
                pole.light1.setState("go")
                pole.light2.setState("go")

            for pole in self.evenPoles:
                pole.light1.setState("stop")
                pole.light2.setState("stop")


    def evenStraightFlow(self, fc):
        if fc - self.prevfc < 360:
            for pole in self.poles:
                if pole.light1.state == "go": pole.light1.setState("slow")
                if pole.light2.state == "go": pole.light2.setState("slow")
        else:
            for pole in self.oddPoles:
                pole.light1.setState("stop")
                pole.light2.setState("stop")

            for pole in self.evenPoles:
                pole.light1.setState("go")
                pole.light2.setState("go")


    def oddLeftOnlyFlow(self):
        for pole in self.oddPoles:
            pole.light1.setState("left-green")
            pole.light2.setState("stop")

        for pole in self.evenPoles:
            pole.light1.setState("stop")
            pole.light2.setState("stop")


    def evenLeftOnlyFlow(self):
        for pole in self.evenPoles:
            pole.light1.setState("left-green")
            pole.light2.setState("stop")

        for pole in self.oddPoles:
            pole.light1.setState("stop")
            pole.light2.setState("stop")


    def specificRoadFlow(self, road):
        road -= 1
        self.poles[road].light1.setState("left-green")
        self.poles[road].light2.setState("go")

        for pole in self.poles:
            if self.poles.index(pole) != road:
                pole.light1.setState("stop")
                pole.light2.setState("stop")


    def setAll(self, state):
        for pole in self.poles:
            pole.light1.setState(state)
            pole.light2.setState(state)




