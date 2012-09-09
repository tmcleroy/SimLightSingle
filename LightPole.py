import pygame

pygame.init()

class LightPole:

    def __init__(self, id, l1, l2, x, y, width, height, color):
        self.id = id
        self.light1 = l1
        self.light2 = l2
        self.x = int(x)
        self.y = int(y)
        self.width = width
        self.height = height
        self.color = color


    def display(self, screen):

        lightDiameter = 8
        lightRadius = 4
        
        #draw the pole
        pygame.draw.rect(screen, self.color, (self.x,self.y,self.width,self.height))
        if self.id%2 == 1:
            #draw light 1
            pygame.draw.circle(screen, self.light1.color, (self.x+20,self.y+self.light1.diameter+1), self.light1.diameter)
            #draw light 2
            pygame.draw.circle(screen, self.light2.color, (self.x+60,self.y+self.light2.diameter+1), self.light2.diameter)
        elif self.id%2 == 0:
            #draw light 1
            pygame.draw.circle(screen, self.light1.color, (self.x+self.light1.diameter+1,self.y+20), self.light1.diameter)
            #draw light 2
            pygame.draw.circle(screen, self.light2.color, (self.x+self.light2.diameter+1,self.y+60), self.light2.diameter)
