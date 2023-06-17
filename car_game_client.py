import pygame
from time import sleep
import socket
import pickle
import copy
import time

from player import Player
from movement import Movement
from initialization_data import InitializationData

connected_players = []
pygame_car_images = []

CAR_WIDTH = 49
CAR_HEIGHT = 100
CAR_VELOCITY = 50

WIDTH = 800
HEIGHT = 600


class GameWindow:

    def __init__(self):

        self.run = False
        self.time = 1

        # initialize constants
        self.BG_SPEED = 3

        # set width,height of game window
        self.WIDTH, self.HEIGHT = 800, 600
        self.WIN = pygame.display.set_mode((self.WIDTH, self.HEIGHT))


        # register player on server (assign id and car image)
        # self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.IP_ADDRESS = 'localhost'
        # self.PORT = 50000
        # self.socket.connect((self.IP_ADDRESS, self.PORT))
        # self.player = Player('AbdulRaouf', 'localhost', 0, {"x": None, "y": None}, None, 1)
        # self.socket.sendall(pickle.dumps(self.player))

        # # retrieve player to start game
        # playerObj = pickle.loads(self.socket.recv(2048))
        # self.player = playerObj

        # initialize font module 
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
        self.myEndLine_y_coordinate = -65

        # init Player
        self.myCar = pygame.image.load('img/car_1.png')
        self.player = Player(x_coordinate=0, y_coordinate=0, progress=0, tarteeb=0)

        # init the other Player
        self.otherCar = pygame.image.load('img/car_1.png')
        self.otherPlayer = Player(x_coordinate=0, y_coordinate=0, progress=0, tarteeb=0)

        # init progress and position
        self.displayProgress()
        self.displayRank()

    def client_initiliazation(self, initialization_data: InitializationData):
        currentPlayerIndex = initialization_data.index
        self.player.x_coordinate = initialization_data.car_data_list[currentPlayerIndex].start_x
        self.player.y_coordinate = initialization_data.car_data_list[currentPlayerIndex].start_y
        self.player.IpAddress = initialization_data.car_data_list[currentPlayerIndex].IpAddress

        self.myCar = pygame.image.load(initialization_data.car_data_list[currentPlayerIndex].carImage)

        otherPlayerIndex = None

        if currentPlayerIndex == 0:
            otherPlayerIndex = 1
        elif currentPlayerIndex == 1:
            otherPlayerIndex = 0

        self.otherPlayer.x_coordinate = initialization_data.car_data_list[otherPlayerIndex].start_x
        self.otherPlayer.y_coordinate = initialization_data.car_data_list[otherPlayerIndex].start_y
        self.otherPlayer.IpAddress = initialization_data.car_data_list[otherPlayerIndex].IpAddress

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

            movement = Movement(left=False, right=False, up=False, down=False, x_coordinate=previous_x_coordinate, y_coordinate=previous_y_coordinate)

            # check for car movements in road
            if keys[pygame.K_LEFT]:
                movement.left = True

            if keys[pygame.K_RIGHT]:
                movement.right = True

            if keys[pygame.K_UP]:
                movement.up = True

            if keys[pygame.K_DOWN]:
                movement.down = True

            # Check if enough time has passed since the last movement update
            if time.time() - last_sent_time >= send_delay:
                # send the movement list
                game_socket.sendall(movement.to_pickle())
                last_sent_time = time.time()  # Update the last sent time

            # Add a small delay to control the frequency of movement updates
            time.sleep(0.1)

    def update_player_data(self, player: Player):
        if player.IpAddress == self.player.IpAddress:
            self.player = player

        elif player.IpAddress == self.otherPlayer.IpAddress:
            self.otherPlayer = player

    def displayProgress(self):
        FONT = pygame.font.SysFont("comicsans", 24)
        progress = FONT.render(f"Progress: {self.player.progress}", True, (255, 255, 255))
        self.WIN.blit(progress, (30, 30))
        pygame.display.update()

    def displayRank(self):
        FONT = pygame.font.SysFont("verdana", 24)
        position = FONT.render(f"Rank: {self.player.tarteeb}", True, (255, 255, 255))
        self.WIN.blit(position, (30, 60))
        pygame.display.update()

    @staticmethod
    def handle_movements_server(movements: Movement, ip_address: str):

        player = Player(x_coordinate=movements.x_coordinate, y_coordinate=movements.y_coordinate, progress=0, tarteeb=0, ip_address=ip_address)

        # check for car movements in road
        if movements.left and movements.x_coordinate - CAR_VELOCITY >= 0:
            player.x_coordinate -= CAR_VELOCITY

        if movements.right and movements.x_coordinate + CAR_VELOCITY + CAR_WIDTH <= WIDTH:
            player.x_coordinate += CAR_VELOCITY


        if movements.up and movements.y_coordinate - CAR_VELOCITY >= 0:
            player.y_coordinate -= CAR_VELOCITY

        if movements.down and movements.y_coordinate + CAR_VELOCITY + CAR_HEIGHT <= HEIGHT:
            player.y_coordinate += CAR_VELOCITY

        return player

    def startRace(self):
        run = False
        players = pickle.loads(self.socket.recv(2048))
        print("Players: ", players)
        run = True
        for player in players:
            global connected_players,pygame_car_images
            connected_players.append(player)
            pygame_car_images.append(pygame.image.load(player.car_image))
        print("Connected")
        for player in connected_players:
            print(player)

        while run:
            # Just to configure fps
            self.clock.tick(30)
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
                end_img = pygame.image.load('../Car Racing Game/img/end.png')
                self.myEndLine_y_coordinate += self.BG_SPEED
                self.move(end_img, self.myEndLine_x_coordinate, self.myEndLine_y_coordinate)

            # move car to new coordinates
            # self.move(self.myCar, self.player.coordinates["x"], self.player.coordinates["y"])

            if self.player.coordinates["y"] < self.myEndLine_y_coordinate - 10:
                my_font = pygame.font.SysFont("Arial", 36)
                text_surface = my_font.render("YOU WON!", True, (255, 255, 255))
                self.WIN.blit(text_surface, (self.WIDTH/2, self.HEIGHT/2))
                pygame.display.update()
                sleep(2)
                run = False

            # send player object to server to broadcast to other players
            playerObj = pickle.dumps(self.player)
            self.socket.sendall(playerObj)
            print('I have sent to the server my new coordinates')

            # receive other player movements
            other_players = self.socket.recv(2048)
            if other_players:
                other_players = pickle.loads(other_players)
                connected_players = copy.deepcopy(other_players)
                print('I have received from the server my enemies coordinates')

            self.render_players()
            pygame.display.update()

        # this line will be reached only if run = False
        pygame.quit()

    def start_race(self):
        run = True

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

            if self.player.progress >= 95:
                end_img = pygame.image.load('../Car Racing Game/img/end.png')
                self.myEndLine_y_coordinate += self.BG_SPEED
                self.move(end_img, self.myEndLine_x_coordinate, self.myEndLine_y_coordinate)

            # move car to new coordinates
            self.move_my_car()

            # move car to new coordinates
            self.move_other_car()

            if self.player.y_coordinate < self.myEndLine_y_coordinate - 10:
                my_font = pygame.font.SysFont("Arial", 36)
                text_surface = my_font.render("YOU WON!", True, (255, 255, 255))
                self.WIN.blit(text_surface, (self.WIDTH / 2, self.HEIGHT / 2))
                pygame.display.update()
                sleep(2)
                run = False

            # send player object to server to broadcast to other players
            # playerObj = pickle.dumps(self.player)
            # self.socket.sendall(playerObj)
            # print('I have sent to the server my new coordinates')

            # receive other player movements
            # other_players = self.socket.recv(2048)
            # if other_players:
            #     other_players = pickle.loads(other_players)
            #     connected_players = copy.deepcopy(other_players)
            #     print('I have received from the server my enemies coordinates')

            # self.render_players()
            pygame.display.update()

        # this line will be reached only if run = False
        pygame.quit()

    def draw_street(self):
        self.WIN.blit(self.myRoad, (0, 0))
        pygame.display.update()

    def move_my_car(self):
        self.WIN.blit(self.myCar, (self.player.x_coordinate, self.player.y_coordinate))
        pygame.display.update()

    def move_other_car(self):
        self.WIN.blit(self.otherCar, (self.otherPlayer.x_coordinate, self.otherPlayer.y_coordinate))
        pygame.display.update()

    def move(self, object, x_coord, y_coord):
        self.WIN.blit(object, (x_coord, y_coord))
        pygame.display.update()

    def is_crash(self):
        pass

    def render_players(self):
        for player in connected_players:
            self.move(pygame_car_images[player.id-1], player.coordinates["x"], player.coordinates["y"])


if __name__ == "__main__":
    game = GameWindow()
    # game.startRace()
