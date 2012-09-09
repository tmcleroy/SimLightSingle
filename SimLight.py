import sys, math, pygame, random
from Light import *
from LightPole import *
from Lane import *
from Road import *
from Vehicle import *
from IntersectionController import *

#positioning variables
middleX = width/2
middleY = height/2
roadWidth = 80
laneWidth = 40
poleWidth = 80
poleHeight = 15

#color variables
black = 0, 0, 0
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,244)
grey = (150, 150, 150)

#the list that will contain all cars
cars = []

#initialize pygame, the game library used for visually
#representing the simulation
pygame.init()

#framerate of the simulation. The screen will refresh this
#many times per second
__FRAMERATE = 120

#dimensions of the simulation window
size = width, height = 1280, 720

#initialize the screen surface onto which everything
#will be drawn
screen = pygame.display.set_mode(size)

#create the rectangles and lines that represent roads
r1RectWidth = roadWidth
r1RectHeight = height
r1RectX = (width/2) - (r1RectWidth)
r1RectY = -1
r1Rect = (r1RectX, r1RectY, r1RectWidth, r1RectHeight)
r2RectWidth = width
r2RectHeight = roadWidth
r2RectX = 0
r2RectY = (height/2) - (r2RectHeight)
r2Rect = (r2RectX, r2RectY, r2RectWidth, r2RectHeight)
r3RectWidth = roadWidth
r3RectHeight = height
r3RectX = (width/2)
r3RectY = -1
r3Rect = (r3RectX, r3RectY, r3RectWidth, r3RectHeight)
r4RectWidth = width
r4RectHeight = roadWidth
r4RectX = 0
r4RectY = (height/2)
r4Rect = (r4RectX, r4RectY, r4RectWidth, r4RectHeight)
r1DividerVec2 = [((width/2)-(laneWidth),0),((width/2)-(laneWidth),height)]
r2DividerVec2 = [(0,(height/2)-(laneWidth)),(width,(height/2)-(laneWidth))]
r3DividerVec2 = [((width/2)+(laneWidth),0),((width/2)+(laneWidth),height)]
r4DividerVec2 = [(0,(height/2)+(laneWidth)),(width,(height/2)+(laneWidth))]


#create the lightpoles
lp1X = middleX - roadWidth
lp1Y = middleY + roadWidth
lp1Width = poleWidth
lp1Height = poleHeight
lp1 = LightPole(1, Light(1, "go"), Light(2, "go"), lp1X, lp1Y, lp1Width, lp1Height, grey)
lp2X = middleX - roadWidth - poleHeight
lp2Y = middleY - roadWidth
lp2Width = poleHeight
lp2Height = poleWidth
lp2 = LightPole(2, Light(1, "stop"), Light(2, "stop"), lp2X, lp2Y, lp2Width, lp2Height, grey)
lp3X = middleX
lp3Y = middleY - roadWidth - poleHeight
lp3Width = poleWidth
lp3Height = poleHeight
lp3 = LightPole(3, Light(1, "go"), Light(2, "go"), lp3X, lp3Y, lp3Width, lp3Height, grey)
lp4X = middleX + roadWidth
lp4Y = middleY
lp4Width = poleHeight
lp4Height = poleWidth
lp4 = LightPole(4, Light(1, "stop"), Light(2, "stop"), lp4X, lp4Y, lp4Width, lp4Height, grey)

#create the roads
rd1 = Road(1,Lane(1, ["straight"]),Lane(2, ["straight"]))
rd2 = Road(2,Lane(1, ["straight"]),Lane(2, ["straight"]))
rd3 = Road(3,Lane(1, ["straight"]),Lane(2, ["straight"]))
rd4 = Road(4,Lane(1, ["straight"]),Lane(2, ["straight"]))

#initialize the clock instance which allows me to
#regulate framerate
Clock = pygame.time.Clock()

#a font instance must be initialized so we can render
#text within the game loop
Font = pygame.font.Font(None, 36)

#start the frame count and seconds passed at 0
frameCount = 0
secondsPassed = 0

#create the intersection controller
cont = IntersectionController(lp1, lp2, lp3, lp4, rd1, rd2, rd3, rd4)

#define our function that will spawn cars
def spawnCar(road, lane, os):
    if road.id == 1:
        if   lane.id==1: carX = middleX-(laneWidth*.75)
        elif lane.id==2: carX = middleX-(laneWidth*1.75)
        carY = 0-200+os
        carLength = 40
        carWidth = 20
        carColor = red
        carRoad = road
        carLane = lane
        carPole = lp1
        carLight = lp1.light2
        carDir = "forward"
        carNext = carLane.getLastVehicle()
        car = Vehicle(carX, carY, carLength, carWidth, carColor, carRoad, carLane, carPole, carLight, carDir, carNext)
        carLane.vehicles.append(car)
        cars.append(car)
    elif road.id == 2:
        if   lane.id==1: carY = middleY-(laneWidth*.75)
        elif lane.id==2: carY = middleY-(laneWidth*1.75)
        carX = width+200+os
        carLength = 20
        carWidth = 40
        carColor = red
        carRoad = road
        carLane = lane
        carPole = lp2
        carLight = lp2.light2
        carDir = "forward"
        carNext = carLane.getLastVehicle()
        car = Vehicle(carX, carY, carLength, carWidth, carColor, carRoad, carLane, carPole, carLight, carDir, carNext)
        carLane.vehicles.append(car)
        cars.append(car)
    elif road.id == 3:
        if   lane.id==1: carX = middleX+(laneWidth*.25)
        elif lane.id==2: carX = middleX+(laneWidth*1.25)
        carY = height+200+os
        carLength = 40
        carWidth = 20
        carColor = red
        carRoad = road
        carLane = lane
        carPole = lp3
        carLight = lp3.light2
        carDir = "forward"
        carNext = carLane.getLastVehicle()
        car = Vehicle(carX, carY, carLength, carWidth, carColor, carRoad, carLane, carPole, carLight, carDir, carNext)
        carLane.vehicles.append(car)
        cars.append(car)
    elif road.id == 4:
        if   lane.id==1: carY = middleY+(laneWidth*.25)
        elif lane.id==2: carY = middleY+(laneWidth*1.25)
        carX = -200+os
        carLength = 20
        carWidth = 40
        carColor = red
        carRoad = road
        carLane = lane
        carPole = lp4
        carLight = lp4.light2
        carDir = "forward"
        carNext = carLane.getLastVehicle()
        car = Vehicle(carX, carY, carLength, carWidth, carColor, carRoad, carLane, carPole, carLight, carDir, carNext)
        carLane.vehicles.append(car)
        cars.append(car)




#spawnCar(1)
#spawnCar(2)

#GAME LOOP. This will run every frame until the
#program is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit();

    #the screen must be erased every frame, the additional
    #elements are then redrawn over the white surface after their
    #positions are recalculated. This creates the illusion of motion
    screen.fill(white)

    #limit framerate
    ms = Clock.tick(__FRAMERATE)

    #increment frame count
    frameCount += 1

    #track seconds passed
    if frameCount % __FRAMERATE == 0:
        secondsPassed += 1

    #every 6 seconds
    if frameCount % (__FRAMERATE*6) == 0:
        spawnCar(rd2, rd2.lane1, random.randint(-100, 100))
        spawnCar(rd2, rd2.lane2, random.randint(-100, 100))
        spawnCar(rd4, rd4.lane1, random.randint(-100, 100))
        spawnCar(rd4, rd4.lane2, random.randint(-100, 100))

    #every 2 seconds
    if frameCount % (__FRAMERATE*2) == 0:
        spawnCar(rd1, rd1.lane1, random.randint(-100, 100))
        spawnCar(rd1, rd1.lane2, random.randint(-100, 100))
        spawnCar(rd3, rd3.lane1, random.randint(-100, 100))
        spawnCar(rd3, rd3.lane2, random.randint(-100, 100))    


    #generates the info text labels. These must be
    #in multiple labels because the font renderer
    #cannot handle newline characters
    fpsText = ("FPS: "+str(int(Clock.get_fps())))
    fpsLabel = Font.render(fpsText, 1, black)
    r1Text = ("Road1: "+str(cont.road1.getNumVehicles()))
    r1Label = Font.render(r1Text, 1, black)
    r2Text = ("Road2: "+str(cont.road2.getNumVehicles()))
    r2Label = Font.render(r2Text, 1, black)
    r3Text = ("Road3: "+str(cont.road3.getNumVehicles()))
    r3Label = Font.render(r3Text, 1, black)
    r4Text = ("Road4: "+str(cont.road4.getNumVehicles()))
    r4Label = Font.render(r4Text, 1, black)
    secondsText = ("Seconds Passed: "+str(secondsPassed))
    secondsLabel = Font.render(secondsText, 1, black)
    

    #draw the shapes that make up the intersection
    pygame.draw.rect(screen, black, r1Rect, 2)
    pygame.draw.rect(screen, black, r2Rect, 2)
    pygame.draw.rect(screen, black, r3Rect, 2)
    pygame.draw.rect(screen, black, r4Rect, 2)
    pygame.draw.lines(screen, black, False, r1DividerVec2, 1)
    pygame.draw.lines(screen, black, False, r2DividerVec2, 1)
    pygame.draw.lines(screen, black, False, r3DividerVec2, 1)
    pygame.draw.lines(screen, black, False, r4DividerVec2, 1)




    cont.auto(frameCount, "mostPopulated")
    
    for car in cars:
        car.display(screen)
        car.auto()
        if car.isOutOfBounds(): cars.remove(car)

    
    #handle keyboard events
    if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if frameCount%10 == 0:
                    spawnCar(rd1, rd1.lane1, 0)
            elif event.key == pygame.K_2:
                if frameCount%10 == 0:
                    spawnCar(rd1, rd1.lane2, 0)
            elif event.key == pygame.K_3:
                if frameCount%10 == 0:
                    spawnCar(rd2, rd2.lane1, 0)
            elif event.key == pygame.K_4:
                if frameCount%10 == 0:
                    spawnCar(rd2, rd2.lane2, 0)
            elif event.key == pygame.K_5:
                if frameCount%10 == 0:
                    spawnCar(rd3, rd3.lane1, 0)
            elif event.key == pygame.K_6:
                if frameCount%10 == 0:
                    spawnCar(rd3, rd3.lane2, 0)
            elif event.key == pygame.K_7:
                if frameCount%10 == 0:
                    spawnCar(rd4, rd4.lane1, 0)
            elif event.key == pygame.K_8:
                if frameCount%10 == 0:
                    spawnCar(rd4, rd4.lane2, 0)
            elif event.key == pygame.K_UP:
                for car in cars:
                    car.move("forward")
            elif event.key == pygame.K_DOWN:
                for car in cars:
                    car.move("reverse")
            elif event.key == pygame.K_a:
                spawnCar(1)
            elif event.key == pygame.K_n:
                for car in cars:
                    car.move("neutral")
            elif event.key == pygame.K_b:
                for car in cars:
                   car.move("brake")
            elif event.key == pygame.K_m:
                cont.setAll("go")
            elif event.key == pygame.K_k:
                cont.setAll("slow")
            elif event.key == pygame.K_o:
                cont.setAll("stop")

    #draw the lightpoles after the cars so the cars appear to
    #be underneath them
    lp1.display(screen)
    lp2.display(screen)
    lp3.display(screen)
    lp4.display(screen)

    
    #display the FPS (Frames Per Second) and info text
    screen.blit(fpsLabel, (0,0))
    screen.blit(r1Label, (0,40))
    screen.blit(r2Label, (0,60))
    screen.blit(r3Label, (0,80))
    screen.blit(r4Label, (0,100))
    screen.blit(secondsLabel, (0, 200))
    
    #update the screen
    pygame.display.flip()

