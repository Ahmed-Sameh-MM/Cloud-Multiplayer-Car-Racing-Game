from player import Player
from movement import Movement

CAR_WIDTH = 49
CAR_HEIGHT = 100
CAR_VELOCITY = 50

WIDTH = 800
HEIGHT = 600


def handle_movements_server(movements: Movement, ip_address: str):
    player = Player(x_coordinate=movements.x_coordinate, y_coordinate=movements.y_coordinate,
                    progress=movements.progress, tarteeb=0,
                    ip_address=ip_address)

    # check for car movements in road
    if movements.left and movements.x_coordinate - CAR_VELOCITY >= 0:
        player.x_coordinate -= CAR_VELOCITY

    if movements.right and movements.x_coordinate + CAR_VELOCITY + CAR_WIDTH <= WIDTH:
        player.x_coordinate += CAR_VELOCITY

    if movements.up and movements.y_coordinate - CAR_VELOCITY >= 0:
        player.y_coordinate -= CAR_VELOCITY

        player.progress = player.progress + 10

    if movements.down and movements.y_coordinate + CAR_VELOCITY + CAR_HEIGHT <= HEIGHT:
        player.y_coordinate += CAR_VELOCITY

        player.progress = player.progress - 10

    return player
