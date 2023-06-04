import pygame
from time import sleep

# 4,5,6 done
pygame.font.init()
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# 10-31 done
myRoad = pygame.transform.scale(pygame.image.load("img/back_ground.jpg"), (WIDTH, HEIGHT))
BG_SPEED = 3

CAR_WIDTH = 49
CAR_HEIGHT = 100

CAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)

def drawGame():
    WIN.blit(myRoad, (0, 0))


def move(object, x_coord, y_coord):
    WIN.blit(object, (x_coord, y_coord))


def updateDisplay():
    pygame.display.update()


def main():
    run = True
    
    # done
    myCar = pygame.image.load("img/car.png")

    myCar_x_coordinate = 200
    myCar_y_coordinate = HEIGHT - CAR_HEIGHT

    myRoad_x1_coordinate = 0
    myRoad_x2_coordinate = 0
    myRoad_y1_coordinate = 0
    myRoad_y2_coordinate = -600

    # enemy_car_1 = pygame.image.load("img/enemy_car_1.png")
    # enemy_car_2 = pygame.image.load("img/enemy_car_2.png")

    # enemyOne_x_coordinate = 370
    # enemyOne_y_coordinate = HEIGHT - CAR_HEIGHT - 10

    # enemyTwo_x_coordinate = 550
    # enemyTwo_y_coordinate = HEIGHT - CAR_HEIGHT - 10

    clock = pygame.time.Clock()

    drawGame()

    move(myCar, myCar_x_coordinate, myCar_y_coordinate)
    move(enemy_car_1, enemyOne_x_coordinate, enemyOne_y_coordinate)
    move(enemy_car_2, enemyTwo_x_coordinate, enemyTwo_y_coordinate)

    while run:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and myCar_x_coordinate - CAR_VEL >= 0:
            myCar_x_coordinate -= CAR_VEL
        if keys[pygame.K_RIGHT] and myCar_x_coordinate + CAR_VEL + CAR_WIDTH <= WIDTH:
            myCar_x_coordinate += CAR_VEL
        if keys[pygame.K_UP] and myCar_y_coordinate - CAR_VEL >= 0:
            myCar_y_coordinate -= CAR_VEL
        if keys[pygame.K_DOWN] and myCar_y_coordinate + CAR_VEL + CAR_HEIGHT <= HEIGHT:
            myCar_y_coordinate += CAR_VEL

        move(myRoad, myRoad_x1_coordinate, myRoad_y1_coordinate)
        move(myRoad, myRoad_x2_coordinate, myRoad_y2_coordinate)

        myRoad_y1_coordinate += BG_SPEED
        myRoad_y2_coordinate += BG_SPEED

        if myRoad_y1_coordinate >= HEIGHT:
            myRoad_y1_coordinate = -600
        if myRoad_y2_coordinate >= HEIGHT:
            myRoad_y2_coordinate = -600

        # if myCar_x_coordinate + CAR_WIDTH > enemyOne_x_coordinate \
        #    and myCar_x_coordinate < enemyOne_x_coordinate + CAR_WIDTH \
        #    and myCar_y_coordinate < enemyTwo_y_coordinate :
        #     text = FONT.render("Game OVER!!", True, (255, 255, 255))
        #     WIN.blit(text, (400 - text.get_width() // 2, 240 - text.get_height() // 2))
        #     move(myCar, myCar_x_coordinate, myCar_y_coordinate)
        #     move(enemy_car_1, enemyOne_x_coordinate, enemyOne_y_coordinate)
        #     move(enemy_car_2, enemyTwo_x_coordinate, enemyTwo_y_coordinate)
        #     updateDisplay()
        #     sleep(1)
        #     drawGame()
        #     myCar_x_coordinate = 200
        #     myCar_y_coordinate = HEIGHT - CAR_HEIGHT
        #     move(myCar, 200, HEIGHT - CAR_HEIGHT)
        #     move(enemy_car_1, 370, HEIGHT - CAR_HEIGHT - 10)
        #     move(enemy_car_2, 550, HEIGHT - CAR_HEIGHT - 10)
        #     updateDisplay()

        move(myCar, myCar_x_coordinate, myCar_y_coordinate)
        # move(enemy_car_1, enemyOne_x_coordinate, enemyOne_y_coordinate)
        # move(enemy_car_2, enemyTwo_x_coordinate, enemyTwo_y_coordinate)

        updateDisplay()

    pygame.quit()


if __name__ == "__main__":
    main()
