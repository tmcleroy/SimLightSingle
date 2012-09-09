#define colors
purple = (255, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

class Light:

    def __init__(self, id, state):
        self.id = id
        self.state = state
        self.diameter = 6
        self.radius = 3



        #default color is purple, this indicates
        #that something is wrong
        self.color = purple

        if self.state == "go":
            self.color = green
        elif self.state == "stop":
            self.color = red
        elif self.state == "slow":
            self.color = yellow


    def setState(self, state):
        self.state = state

        if self.state == "go":
            self.color = green
        elif self.state == "stop":
            self.color = red
        elif self.state == "slow":
            self.color = yellow
