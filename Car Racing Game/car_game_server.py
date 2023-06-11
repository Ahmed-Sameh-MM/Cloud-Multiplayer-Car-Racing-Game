import pygame
from time import sleep
import sys

sys.path.append('../')
import player



class Car:

    def __init__(self):

        self.run = False
        self.time = 1

        # initialize font module 
        pygame.font.init()
        self.FONT = pygame.font.SysFont("comicsans", 60)

        # set width,height of game window
        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        # set background and car images
        self.myRoad = pygame.transform.scale(pygame.image.load("img/back_ground.jpg"), (self.WIDTH, self.HEIGHT))
       
        # initialize constants
        self.BG_SPEED = 3
        self.CAR_WIDTH = 49
        self.CAR_HEIGHT = 100
        self.CAR_VEL = 5

        # draw background image
        self.drawStreet()

        # initialize clock object
        self.clock = pygame.time.Clock()

        # set up initial coordinates for road in the game
        self.myRoad_x1_coordinate = 0
        self.myRoad_x2_coordinate = 0
        self.myRoad_y1_coordinate = 0
        self.myRoad_y2_coordinate = -600

        # set up initial coordinated for end line in the game
        self.myEndLine_x_coordinate = 150
        self.myEndLine_y_coordinate = -65


        # init player.Player
        self.player = player.Player('AbdulRaouf','localhost',0,{"x": 200, "y": self.HEIGHT-self.CAR_HEIGHT},'img/car.png',1)
        self.myCar = pygame.image.load(self.player.car_image)

        # init progress and position
        self.displayProgress()
        self.displayRank()
    
    def displayProgress(self):
        FONT = pygame.font.SysFont("comicsans", 24)
        progress = FONT.render(f"Progress: {self.player.progress}", True, (255,255,255))
        self.WIN.blit(progress,(30,30))
        pygame.display.update()

    def displayRank(self):
        FONT = pygame.font.SysFont("verdana", 24)
        position = FONT.render(f"Rank: {self.player.position}", True, (255,255,255))
        self.WIN.blit(position,(30,60))
        pygame.display.update()
    
    def handleMovements(self):
        keys = pygame.key.get_pressed()

        # check for car movements in road
        if keys[pygame.K_LEFT] and self.player.coordinates["x"] - self.CAR_VEL >= 0:
            self.player.coordinates["x"] -= self.CAR_VEL
        if keys[pygame.K_RIGHT] and self.player.coordinates["x"] + self.CAR_VEL + self.CAR_WIDTH <= self.WIDTH:
            self.player.coordinates["x"] += self.CAR_VEL
        if keys[pygame.K_UP] and self.player.Player.coordinates["y"] - self.CAR_VEL >= 0:
            self.player.coordinates["y"] -= self.CAR_VEL
        if keys[pygame.K_DOWN] and self.player.coordinates["y"] + self.CAR_VEL + self.CAR_HEIGHT <= self.HEIGHT:
            self.player.coordinates["y"] += self.CAR_VEL

    def startRace(self):
        run = True
        # This while loop is required in every pygame instance that keeps the game in the
        # running state
        while run:
            # Just to configure fps
            self.clock.tick(60)
            self.displayProgress()
            if pygame.time.get_ticks() >= 300 * self.time:
                self.displayProgress()
                if self.player.progress < 100:
                    self.player.progress += 1 
                self.time += 1
            self.displayRank()
            # checking for key events
            for event in pygame.event.get():
                # if quit button is clicked
                # break out of this while loop and stop pygame instance
                if event.type == pygame.QUIT:
                    run = False
                    break
            
            self.handleMovements()

            # move the street down the window
            self.move(self.myRoad, self.myRoad_x1_coordinate, self.myRoad_y1_coordinate)
            self.move(self.myRoad, self.myRoad_x2_coordinate, self.myRoad_y2_coordinate)

            
            self.myRoad_y1_coordinate += self.BG_SPEED
            self.myRoad_y2_coordinate += self.BG_SPEED

            if self.myRoad_y1_coordinate >= self.HEIGHT:
                self.myRoad_y1_coordinate = -600
            if self.myRoad_y2_coordinate >= self.HEIGHT:
                self.myRoad_y2_coordinate = -600

            if self.player.progress >= 95:
                end_img = pygame.image.load('img/end.png')
                self.myEndLine_y_coordinate += self.BG_SPEED
                self.move(end_img,self.myEndLine_x_coordinate,self.myEndLine_y_coordinate)

            # move car to new coordinates
            self.move(self.myCar, self.player.coordinates["x"], self.player.coordinates["y"])

           
            
            if self.player.coordinates["y"] < self.myEndLine_y_coordinate - 10:
                my_font = pygame.font.SysFont("Arial", 36)
                text_surface = my_font.render("YOU WON!", True, (255, 255, 255))
                self.WIN.blit(text_surface, (self.WIDTH/2, self.HEIGHT/2))
                pygame.display.update()
                sleep(2)
                run = False
            # This line of code is required to render changes on the screen 
            pygame.display.update()
        
        # this line will be reached only if run = False
        pygame.quit()

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
    
    
