import pygame
from time import sleep

class Car:

    def __init__(self):

        self.run = False

        # initialize font module 
        pygame.font.init()
        self.FONT = pygame.font.SysFont("comicsans", 60)

        # set width,height of game window
        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # set background and car images
        self.myRoad = pygame.transform.scale(pygame.image.load("img/back_ground.jpg"), (self.WIDTH, self.HEIGHT))
        self.myCar = pygame.image.load("img/car.png")

        # initialize constants
        self.BG_SPEED = 3
        self.CAR_WIDTH = 49
        self.CAR_HEIGHT = 100
        self.CAR_VEL = 5

        # draw background image
        self.drawStreet()

        # initialize clock object
        self.clock = pygame.time.Clock()

        # set up initial coordinates for all objects in the game
        self.myCar_x_coordinate = 200
        self.myCar_y_coordinate = self.HEIGHT - self.CAR_HEIGHT

        self.myRoad_x1_coordinate = 0
        self.myRoad_x2_coordinate = 0
        self.myRoad_y1_coordinate = 0
        self.myRoad_y2_coordinate = -600

    def startRace(self):
        run = True
        while run:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.myCar_x_coordinate - self.CAR_VEL >= 0:
                self.myCar_x_coordinate -= self.CAR_VEL
            if keys[pygame.K_RIGHT] and self.myCar_x_coordinate + self.CAR_VEL + self.CAR_WIDTH <= self.WIDTH:
                self.myCar_x_coordinate += self.CAR_VEL
            if keys[pygame.K_UP] and self.myCar_y_coordinate - self.CAR_VEL >= 0:
                self.myCar_y_coordinate -= self.CAR_VEL
            if keys[pygame.K_DOWN] and self.myCar_y_coordinate + self.CAR_VEL + self.CAR_HEIGHT <= self.HEIGHT:
                self.myCar_y_coordinate += self.CAR_VEL

            self.move(self.myRoad, self.myRoad_x1_coordinate, self.myRoad_y1_coordinate)
            self.move(self.myRoad, self.myRoad_x2_coordinate, self.myRoad_y2_coordinate)

            self.myRoad_y1_coordinate += self.BG_SPEED
            self.myRoad_y2_coordinate += self.BG_SPEED

            if self.myRoad_y1_coordinate >= self.HEIGHT:
                self.myRoad_y1_coordinate = -600
            if self.myRoad_y2_coordinate >= self.HEIGHT:
                self.myRoad_y2_coordinate = -600
            
            self.move(self.myCar, self.myCar_x_coordinate, self.myCar_y_coordinate)

            pygame.display.update()

    def drawStreet(self):
        self.WIN.blit(self.myRoad, (0, 0))
        pygame.display.update()
        
    
    def move(self, object, x_coord, y_coord):
        self.WIN.blit(object, (x_coord, y_coord))

    def isCrash():
        pass

if __name__ == "__main__":
    car = Car()
    car.startRace()
    
    
