import pygame, math
pygame.init()



size = width, height = 1280, 720

#positioning variables
middleX = int(width/2)
middleY = int(height/2)
roadWidth = 80
laneWidth = 40
poleWidth = 80
poleHeight = 15

#should be 39 according to the equation
#Pixels to stop = 39 * speed
eq = 39

#degrees in radians that define car movement direction
up = 0
down = math.pi
left = math.pi/2
right = (3*math.pi)/2

#maximum allowed distance between vehicles
vehicleSpace = 5
baseSpeed = 0.001
greenSpeed = 10
yellowSpeed = 3
vehicStop = None
killDistance = 100

class Vehicle:
    #CONSTRUCTOR
    def __init__(self, x, y, l, w, color, image, road, lane, pole, light, direction, nextVehic):
        self.x = x
        self.y = y
        self.length = l
        self.width = w
        self.color = color
        self.road = road
        self.pole = pole
        self.light = light
        self.lane = lane
        self.direction = direction

        #these parameters control the physics of the car
        self.speed = baseSpeed
        self.mass = 1
        self.massOfAir = 0.15
        self.acceleration = 1
        self.drag = self.mass/(self.mass + self.massOfAir)
        self.maxSpeed = 10

        #this is the vehicle in front of the current one
        #the position of this vehicle is used to prevent collision
        self.nextVehic = nextVehic


        #set the front facing direction of the vehicle
        #depending on its road, the poleStop value
        #which tells the vehicles where they need to stop at lights
        #and properly rotate or flip the vehicle image
        if self.road.id==1:
            self.angle = down
            self.poleStop = self.pole.y-(roadWidth*2)-self.length
            self.poleSlow = self.poleStop/2
            self.image = pygame.image.load(image)
            self.rect = self.image.get_rect()
        elif self.road.id==2:
            self.angle = left
            self.poleStop = self.pole.x+(roadWidth*2)+poleHeight
            self.image = pygame.transform.rotate(pygame.image.load(image),270)
            self.rect = self.image.get_rect()
        elif self.road.id==3:
            self.angle = up
            self.poleStop = self.pole.y+(roadWidth*2)+poleHeight
            self.image = pygame.transform.flip(pygame.image.load(image), False, True)
            self.rect = self.image.get_rect()
        elif self.road.id==4:
            self.angle = right
            self.poleStop = self.pole.x-(roadWidth*2)-self.width
            self.image = pygame.transform.rotate(pygame.image.load(image),90)
            self.rect = self.image.get_rect()




        
    #this is the decision making method that asks questions of the other methods
    #and decides to move forward, brake, or remove itself from the vehicle list
    def auto(self):
        #if the vehicle is past the stop line and is in
        #the lanes list of vehicles
        if self.isPastLine() and self in self.lane.vehicles:
            self.lane.vehicles.remove(self)
        #accelerate if possible
        if self.canGo():
            self.move("forward")
        elif not self.canGo():
            self.move("brake")



    #this method draws the vehicle to the screen
    def display(self, screen):
        #pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.length))
        self.rect.x = self.x
        self.rect.y = self.y
        screen.blit(self.image, self.rect)

        

    #this method calculates the next position of the vehicle based on the physics parameters
    def move(self, direction):
        if direction == "forward":
            if self.speed < baseSpeed: self.speed = baseSpeed
            self.acceleration += .1
            #higher value, higher acceleration
            if self.acceleration >= self.massOfAir+1+.05: self.acceleration = self.massOfAir+1+.05
            self.speed = (self.speed * self.drag * self.acceleration)
            if self.speed >= self.maxSpeed: self.speed = self.maxSpeed
            if self.road.id%2 == 1 and self.speed>baseSpeed:
                self.y -= math.cos(self.angle) * self.speed
            elif self.road.id % 2 == 0 and self.speed>baseSpeed:
                self.x -= math.sin(self.angle) * self.speed
                
        elif direction == "brake":
            self.acceleration -= .1
            #higher value, lower braking power
            if self.acceleration <= self.massOfAir+1-.04: self.acceleration = self.massOfAir+1-.04
            self.speed = (self.speed * self.drag * self.acceleration)
            if self.speed <= baseSpeed: self.speed = baseSpeed
            if self.road.id%2 == 1 and self.speed>baseSpeed:
                self.y -= math.cos(self.angle) * self.speed
            elif self.road.id%2 == 0 and self.speed>baseSpeed:
                self.x -= math.sin(self.angle) * self.speed



    #this method determines whether or not the vehicle has passed the stop line
    def isPastLine(self):
        if   self.road.id==1:return self.y > self.poleStop
        elif self.road.id==2:return self.x < self.poleStop
        elif self.road.id==3:return self.y < self.poleStop
        elif self.road.id==4:return self.x > self.poleStop

    def isOutOfBounds(self):
        if   self.road.id==1:return self.y > height+100
        elif self.road.id==2:return self.x < 0-100
        elif self.road.id==3:return self.y < 0-100
        elif self.road.id==4:return self.x > width+100



    #this method determines whether or not a vehicle can accelerate
    #it is only so long because it must contain 4 slightly different
    #versions of the same code
    def canGo(self):
        if self.road.id == 1:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.y-self.length-vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (self.poleStop-self.y) >= (eq*self.speed) and (vehicStop-self.y) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (self.poleStop-self.y) >= (eq*self.speed):
                        return True
                return False
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y-self.length-vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (vehicStop-self.y) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                return False
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y-self.length-vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (vehicStop-self.y) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                return False
            
        elif self.road.id == 2:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.x+self.width+vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed) and (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed):
                        return True
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x+self.width+vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x+self.width+vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                
        elif self.road.id == 3:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.y+self.length+vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(self.poleStop-self.y)) >= (eq*self.speed) and (abs(vehicStop-self.y)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (abs(self.poleStop-self.y)) >= (eq*self.speed):
                        return True
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y+self.length+vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(vehicStop-self.y)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.y+self.length+vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(vehicStop-self.y)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
                
        elif self.road.id == 4:
            if self.light.state == "stop":
                self.maxSpeed = greenSpeed
                #the car may go if it has already passed the line
                #this avoids collisions in the middle of the intersection
                if self.isPastLine(): return True
                #if there is a vehicle in front of me
                if self.nextVehic:
                    vehicStop = self.nextVehic.x-self.width-vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed) and (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    #same check but without the vehicle
                    if (abs(self.poleStop-self.x)) >= (eq*self.speed):
                        return True
            elif self.light.state == "go":
                self.maxSpeed = greenSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x-self.width-vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
            elif self.light.state == "slow":
                if self.isPastLine(): self.maxSpeed = greenSpeed
                else: self.maxSpeed = yellowSpeed
                if self.isPastLine(): return True
                if self.nextVehic:
                    vehicStop = self.nextVehic.x-self.width-vehicleSpace
                    #check if i have enough room to stop if i need to
                    if (abs(vehicStop-self.x)) >= (eq*self.speed):
                        return True
                #if there is no car in front of me
                elif not self.nextVehic:
                    return True
        return False
        

    #a utility method for visually marking areas of the screen
    def showCircle(self, screen, color, circle, radius):
        pygame.draw.circle(screen, color, circle, radius)
