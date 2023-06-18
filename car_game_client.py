import pygame
from time import sleep
import socket
import time

from player import Player
from movement import Movement
from initialization_data import InitializationData

connected_players = []
pygame_car_images = []

END_MESSAGE = ''


class GameWindow:

    def __init__(self):

        self.run = False

        # initialize constants
        self.BG_SPEED = 3

        # set width,height of game window
        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

        pygame.font.init()
        self.FONT = pygame.font.SysFont("comicsans", 60)

        # set background and car images
        self.myRoad = pygame.transform.scale(pygame.image.load("img/back_ground.jpg"), (self.WIDTH, self.HEIGHT))

        # draw background image
        self.draw_street()

        # initialize clock object
        self.clock = pygame.time.Clock()

        # set up initial coordinates for road in the game
        self.myRoad_x1_coordinate = 0
        self.myRoad_x2_coordinate = 0
        self.myRoad_y1_coordinate = 0
        self.myRoad_y2_coordinate = -600

        # set up initial coordinated for end line in the game
        self.myEndLine_x_coordinate = 150
        self.myEndLine_y_coordinate = 50

        # init Player
        self.myCar = None
        self.player = Player(x_coordinate=0, y_coordinate=0, progress=0, tarteeb=0)

        # init the other Player
        self.otherCar = None
        self.otherPlayer = Player(x_coordinate=0, y_coordinate=0, progress=0, tarteeb=0)

        # init progress and position
        self.display_progress()
        self.display_rank()

        self.draw_street()

        pygame.display.set_caption("🌫️CLOUD‍️‍🌫️ car racing game")

        pygame.display.update()

    def client_initiliazation(self, initialization_data: InitializationData):
        currentPlayerIndex = initialization_data.index
        self.player.x_coordinate = initialization_data.car_data_list[currentPlayerIndex].start_x
        self.player.y_coordinate = initialization_data.car_data_list[currentPlayerIndex].start_y
        self.player.IpAddress = initialization_data.car_data_list[currentPlayerIndex].IpAddress
        self.player.progress = initialization_data.car_data_list[currentPlayerIndex].progress

        self.myCar = pygame.image.load(initialization_data.car_data_list[currentPlayerIndex].carImage)

        otherPlayerIndex = None

        if currentPlayerIndex == 0:
            otherPlayerIndex = 1
        elif currentPlayerIndex == 1:
            otherPlayerIndex = 0

        self.otherPlayer.x_coordinate = initialization_data.car_data_list[otherPlayerIndex].start_x
        self.otherPlayer.y_coordinate = initialization_data.car_data_list[otherPlayerIndex].start_y
        self.otherPlayer.IpAddress = initialization_data.car_data_list[otherPlayerIndex].IpAddress
        self.otherPlayer.progress = initialization_data.car_data_list[otherPlayerIndex].progress

        self.otherCar = pygame.image.load(initialization_data.car_data_list[otherPlayerIndex].carImage)

        self.move_my_car()

        self.move_other_car()

    def handle_movements(self, game_socket: socket.socket):
        send_delay = 1  # Adjust this value to control the delay between movement updates
        last_sent_time = time.time()

        while True:
            keys = pygame.key.get_pressed()

            previous_x_coordinate = self.player.x_coordinate
            previous_y_coordinate = self.player.y_coordinate

            movement = Movement(left=False, right=False, up=False, down=False, x_coordinate=previous_x_coordinate,
                                y_coordinate=previous_y_coordinate, progress=self.player.progress)

            # check for car movements in road
            if keys[pygame.K_LEFT]:
                movement.left = True

            if keys[pygame.K_RIGHT]:
                movement.right = True

            if keys[pygame.K_UP]:
                movement.up = True

            if keys[pygame.K_DOWN]:
                movement.down = True

            if not (movement.left or movement.right or movement.up or movement.down):
                continue

            # Check if enough time has passed since the last movement update
            if time.time() - last_sent_time >= send_delay:
                # send the movement list
                game_socket.sendall(movement.to_pickle())
                last_sent_time = time.time()  # Update the last sent time

            # Add a small delay to control the frequency of movement updates
            time.sleep(0.1)

    def update_player_data(self, player: Player):
        global END_MESSAGE

        player_rank = player.tarteeb

        other_player_rank = 2 if player_rank == 1 else 1

        if player.IpAddress == self.player.IpAddress:
            self.player = player

            self.otherPlayer.tarteeb = other_player_rank

        elif player.IpAddress == self.otherPlayer.IpAddress:
            self.otherPlayer = player

            self.player.tarteeb = other_player_rank

        if self.player.progress == 100:
            END_MESSAGE = 'U WON !'

        elif self.otherPlayer.progress == 100:
            END_MESSAGE = 'U LOST :('

    def display_progress(self):
        FONT = pygame.font.SysFont("comicsans", 24)
        progress = FONT.render(f"Progress: {self.player.progress}", True, (255, 255, 255))
        self.WIN.blit(progress, (30, 30))

    def display_rank(self):
        FONT = pygame.font.SysFont("verdana", 24)
        position = FONT.render(f"Rank: {self.player.tarteeb}", True, (255, 255, 255))
        self.WIN.blit(position, (30, 60))

    def start_race(self):
        run = True

        while run:
            # Just to configure fps
            self.clock.tick(60)

            # checking for key events
            for event in pygame.event.get():
                # if quit button is clicked
                # break out of this while loop and stop pygame instance
                if event.type == pygame.QUIT:
                    run = False
                    break

            # self.handleMovements()

            # move the street down the window
            self.move(self.myRoad, self.myRoad_x1_coordinate, self.myRoad_y1_coordinate)
            self.move(self.myRoad, self.myRoad_x2_coordinate, self.myRoad_y2_coordinate)

            self.myRoad_y1_coordinate += self.BG_SPEED
            self.myRoad_y2_coordinate += self.BG_SPEED

            if self.myRoad_y1_coordinate >= self.HEIGHT:
                self.myRoad_y1_coordinate = -600
            if self.myRoad_y2_coordinate >= self.HEIGHT:
                self.myRoad_y2_coordinate = -600

            if self.player.progress >= 70:
                end_img = pygame.image.load('img/end.png')
                self.move(end_img, self.myEndLine_x_coordinate, self.myEndLine_y_coordinate)

            # move car to new coordinates
            self.move_my_car()

            # move car to new coordinates
            self.move_other_car()

            if self.player.progress == 100:
                my_font = pygame.font.SysFont("Arial", 100)
                text_surface = my_font.render(END_MESSAGE, True, (255, 0, 0))
                self.WIN.blit(text_surface, (200, self.HEIGHT / 2))

                pygame.display.update()

                sleep(5)
                run = False

            # self.render_players()
            self.display_progress()
            self.display_rank()
            pygame.display.update()

        # this line will be reached only if run = False
        pygame.quit()

    def draw_street(self):
        self.WIN.blit(self.myRoad, (0, 0))

    def move_my_car(self):
        self.WIN.blit(self.myCar, (self.player.x_coordinate, self.player.y_coordinate))

    def move_other_car(self):
        self.WIN.blit(self.otherCar, (self.otherPlayer.x_coordinate, self.otherPlayer.y_coordinate))

    def move(self, object, x_coord, y_coord):
        self.WIN.blit(object, (x_coord, y_coord))

    def is_crash(self):
        pass
