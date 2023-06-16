import socket
from threading import Thread
import pickle
import random
from typing import List

from player import Player

MAIN_SERVER_HOST = 'localhost'
MAIN_SERVER_PORT = 50000

# Player Constants
ID = 1
START_X: int = 200
START_Y: int = 395

LISTENER_LIMIT = 3
active_players: List[Player] = []
disconnected_players: List[Player] = []
car_images = ['img/car_1.png', 'img/car_2.png', 'img/car_3.png', 'img/car_4.jpeg', 'img/car_5.jpeg']


def send_message(player_socket: socket.socket):
    global active_players
    player_socket.sendall(pickle.dumps(active_players))


def broadcast_message(player: Player):
    print("hello from broadcast")
    for active_player in active_players:
        if active_player.id != player.id:
            send_message(active_player.socket)
    print("Server successfully broadcasted the player movements to other players")


def handle_player(player_socket, playerObj):
    try:
        global active_players
        while not player_socket.recv(2048): 
                active_players[playerObj.id-1].coordinates["x"], active_players[playerObj.id].coordinates["y"] = playerObj.coordinates["x"], playerObj.coordinates["y"]
                broadcast_message(playerObj)
        # print("Handling Done")
    except:
        print("Player could not handled")
    return


def on_init(player_socket: socket.socket, playerObj):
    global ID, active_players, START_X, START_Y
    playerObj.id = ID
    ID += 1
    random_num = random.randint(0, len(car_images)-1)
    playerObj.car_image = car_images[random_num]
    playerObj.coordinates["x"] = START_X
    playerObj.coordinates["y"] = START_Y
    START_X += 30
    car_images.pop(random_num)
    active_players.append(playerObj)
    id = playerObj.id
    playerObj = pickle.dumps(playerObj)
    player_socket.sendall(playerObj)
    print(f"Player {id} has been registered in the server")


def check_players(player_socket: socket.socket):
    print("Active:", active_players)
    while True:
        print(f"Client {ID} checks for all players")
        if len(active_players) == 2:
            player_socket.sendall(pickle.dumps(active_players))
            break


def receive_player_obj(player_socket):
    while True:
        playerObj = pickle.loads(player_socket.recv(2048))
        if playerObj == "Are all players connected ?":
                Thread(target=check_players, args=(player_socket,)).start()
        elif playerObj.id is None:
            Thread(target=on_init, args=(player_socket, playerObj)).start()
        else:
            print("calling handle")
            Thread(target=handle_player, args=(player_socket, playerObj)).start()


def check_players_2(player_socket: socket.socket, player_obj: Player):
    print("Active:", active_players)
    player_obj = pickle.loads(player_obj)
    print(f"Client {player_obj.id} checks for all players")
    while True:
        if len(active_players) == 2:
            player_socket.sendall(pickle.dumps(active_players))
            break

    print("calling handle")
    handle_player(player_socket, player_obj)


def on_init2(player_socket: socket.socket, playerObj):
    global ID, active_players, START_X, START_Y
    playerObj.id = ID
    ID += 1
    random_num = random.randint(0, len(car_images)-1)
    playerObj.car_image = car_images[random_num]
    playerObj.coordinates["x"] = START_X
    playerObj.coordinates["y"] = START_Y
    START_X += 30
    car_images.pop(random_num)
    active_players.append(playerObj)
    id = playerObj.id
    playerObj = pickle.dumps(playerObj)
    player_socket.sendall(playerObj)
    print(f"Player {id} has been registered in the server")
    check_players_2(player_socket, playerObj)
    

def receive_player_obj_2(player_socket):
    playerObj = pickle.loads(player_socket.recv(2048))
    on_init2(player_socket, playerObj)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((MAIN_SERVER_HOST, MAIN_SERVER_PORT))
        print(f"Running the server_socket on {MAIN_SERVER_HOST}:{MAIN_SERVER_PORT}")
    except:
        print(f"Unable to bind to host {MAIN_SERVER_HOST} and port {MAIN_SERVER_PORT}")

    server_socket.listen(LISTENER_LIMIT)

    while True:
        player_socket, address_info = server_socket.accept()
        print(f"Successfully connected to client {address_info[0]}:{address_info[1]}")
        # Thread(target=receive_player_obj_2, args=(player_socket,)).start()

        if len(active_players) == 2:
            player_socket.sendall(pickle.dumps(active_players))
            break


if __name__ == '__main__':
    main()
