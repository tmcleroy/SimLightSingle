import sys, math, pygame, random
from Light import *
from LightPole import *
from Lane import *
from Road import *
from Vehicle import *
from IntersectionController import *


#color and filename variables
black = 0, 0, 0
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,244)
yellow = (255,255,0)
grey = (150, 150, 150)
dark_grey = (90, 95, 90)
fname = "car.png"

#positioning variables
middleX = width/2
middleY = height/2
roadWidth = 80
laneWidth = 40
poleWidth = 80
poleHeight = 15
poleColor = dark_grey


#the list that will contain all cars
cars = []
roads = []
medians = []
divs = []
poles = []

#the list I will use to keep track of the number
#of cars that pass through the intersection
passed = [0,0,0,0]

#initialize pygame, the game library used for visually
#representing the simulation
pygame.init()

#framerate of the simulation. The screen will refresh this
#many times per second
framerate = 120

#dimensions of the simulation window
size = width, height = 1280, 720

#initialize the screen surface onto which everything
#will be drawn
screen = pygame.display.set_mode(size)

#create the rectangles and lines that represent roads
r1Width = roadWidth
r1Height = height
r1X = (width/2) - (r1Width)
r1Y = -1
r1 = (r1X, r1Y, r1Width, r1Height)
r2Width = width
r2Height = roadWidth
r2X = 0
r2Y = (height/2) - (r2Height)
r2 = (r2X, r2Y, r2Width, r2Height)
r3Width = roadWidth
r3Height = height
r3X = (width/2)
r3Y = -1
r3 = (r3X, r3Y, r3Width, r3Height)
r4Width = width
r4Height = roadWidth
r4X = 0
r4Y = (height/2)
r4 = (r4X, r4Y, r4Width, r4Height)
roads.append(r1)
roads.append(r2)
roads.append(r3)
roads.append(r4)

medians.append([((width/2),0),((width/2),(height/2)-roadWidth-1)])
medians.append([(width,(height/2)),((width/2)+roadWidth,(height/2))])
medians.append([((width/2),height),((width/2),(height/2)+roadWidth)])
medians.append([(0,(height/2)),((width/2)-roadWidth-1,(height/2))])

for x in range(28):
    divs.append([(20*x+5,(height/2)-laneWidth),(20*x+12,(height/2)-laneWidth)])
    divs.append([(20*x+5,(height/2)+laneWidth),(20*x+12,(height/2)+laneWidth)])
    divs.append([((20*x+5)+(width/2)+roadWidth,(height/2)-laneWidth),((20*x+12)+(width/2)+roadWidth,(height/2)-laneWidth)])
    divs.append([((20*x+5)+(width/2)+roadWidth,(height/2)+laneWidth),((20*x+12)+(width/2)+roadWidth,(height/2)+laneWidth)])
    if x < 14:
        divs.append([((width/2)-laneWidth,20*x+5),((width/2)-laneWidth,20*x+12)])
        divs.append([((width/2)+laneWidth,20*x+5),((width/2)+laneWidth,20*x+12)])
        divs.append([((width/2)-laneWidth,(20*x+5)+(height/2)+roadWidth),((width/2)-laneWidth,(20*x+12)+(height/2)+roadWidth)])
        divs.append([((width/2)+laneWidth,(20*x+5)+(height/2)+roadWidth),((width/2)+laneWidth,(20*x+12)+(height/2)+roadWidth)])

#create the lightpoles
lp1X = middleX - roadWidth
lp1Y = middleY + roadWidth
lp1Width = poleWidth
lp1Height = poleHeight
lp1 = LightPole(1, Light(1, "go"), Light(2, "go"), lp1X, lp1Y, lp1Width, lp1Height, poleColor)
lp2X = middleX - roadWidth - poleHeight
lp2Y = middleY - roadWidth
lp2Width = poleHeight
lp2Height = poleWidth
lp2 = LightPole(2, Light(1, "stop"), Light(2, "stop"), lp2X, lp2Y, lp2Width, lp2Height, poleColor)
lp3X = middleX
lp3Y = middleY - roadWidth - poleHeight
lp3Width = poleWidth
lp3Height = poleHeight
lp3 = LightPole(3, Light(1, "go"), Light(2, "go"), lp3X, lp3Y, lp3Width, lp3Height, poleColor)
lp4X = middleX + roadWidth
lp4Y = middleY
lp4Width = poleHeight
lp4Height = poleWidth
lp4 = LightPole(4, Light(1, "stop"), Light(2, "stop"), lp4X, lp4Y, lp4Width, lp4Height, poleColor)
poles.append(lp1)
poles.append(lp2)
poles.append(lp3)
poles.append(lp4)

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
        car = Vehicle(carX, carY, carLength, carWidth, carColor, fname, carRoad, carLane, carPole, carLight, carDir, carNext)
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
        car = Vehicle(carX, carY, carLength, carWidth, carColor, fname, carRoad, carLane, carPole, carLight, carDir, carNext)
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
        car = Vehicle(carX, carY, carLength, carWidth, carColor, fname, carRoad, carLane, carPole, carLight, carDir, carNext)
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
        car = Vehicle(carX, carY, carLength, carWidth, carColor, fname, carRoad, carLane, carPole, carLight, carDir, carNext)
        carLane.vehicles.append(car)
        cars.append(car)



#GAME LOOP. This will run every frame (120 times per second) until the program is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(); sys.exit();

    #the screen must be erased every frame, the additional
    #elements are then redrawn over the white surface after their
    #positions are recalculated. This creates the illusion of motion
    screen.fill(white)

    #limit framerate
    ms = Clock.tick(framerate)

    #increment frame count and track seconds passed
    frameCount += 1
    if frameCount % framerate == 0: secondsPassed += 1
    
    """
    #every 6 seconds
    if frameCount % (framerate*6) == 0:
        spawnCar(rd2, rd2.lane1, random.randint(-100, 100))
        spawnCar(rd2, rd2.lane2, random.randint(-100, 100))
        spawnCar(rd4, rd4.lane1, random.randint(-100, 100))
        spawnCar(rd4, rd4.lane2, random.randint(-100, 100))

    #every 2 seconds
    if frameCount % (framerate*2) == 0:
        spawnCar(rd1, rd1.lane1, random.randint(-100, 100))
        spawnCar(rd1, rd1.lane2, random.randint(-100, 100))
        spawnCar(rd3, rd3.lane1, random.randint(-100, 100))
        spawnCar(rd3, rd3.lane2, random.randint(-100, 100))    
    """

    #generates the info text labels. These must be
    #in multiple labels because the font renderer
    #cannot handle newline characters
    fpsText = ("FPS: "+str(int(Clock.get_fps())))
    fpsLabel = Font.render(fpsText, 1, black)
    r1Text = ("Road1: "+str(cont.road1.getNumVehicles())+ "...Passed: "+str(passed[0]))
    r1Label = Font.render(r1Text, 1, black)
    r2Text = ("Road2: "+str(cont.road2.getNumVehicles())+ "...Passed: "+str(passed[1]))
    r2Label = Font.render(r2Text, 1, black)
    r3Text = ("Road3: "+str(cont.road3.getNumVehicles())+ "...Passed: "+str(passed[2]))
    r3Label = Font.render(r3Text, 1, black)
    r4Text = ("Road4: "+str(cont.road4.getNumVehicles())+ "...Passed: "+str(passed[3]))
    r4Label = Font.render(r4Text, 1, black)
    secondsText = ("Seconds Passed: "+str(secondsPassed))
    secondsLabel = Font.render(secondsText, 1, black)
    

    #draw the road features
    for road in roads: pygame.draw.rect(screen, grey, road, 0)
    for median in medians: pygame.draw.lines(screen, black, False, median, 3)
    for div in divs: pygame.draw.lines(screen, yellow, False, div, 2)


    cont.auto("mostPopulated")
    
    for car in cars:
        car.display(screen)
        car.auto()
        if car.isOutOfBounds():
            passed[car.road.id-1] += 1
            cars.remove(car) 

    
    #handle keyboard input
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


    #draw the lightpoles after the cars so the cars appear to be underneath them
    for pole in poles: pole.display(screen)

    
    #display the FPS (Frames Per Second) and info text
    screen.blit(fpsLabel, (0,0))
    screen.blit(r1Label, (0,40))
    screen.blit(r2Label, (0,60))
    screen.blit(r3Label, (0,80))
    screen.blit(r4Label, (0,100))
    screen.blit(secondsLabel, (0, 200))
    
    #update the screen
    pygame.display.flip()

