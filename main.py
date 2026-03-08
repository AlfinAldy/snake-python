from tkinter import *
import random

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 120
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
GRID_COLOR = "#222222"

class Snake:

    def __init__(self):

        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        for i in range(BODY_PARTS):
            self.coordinates.append([0, 0])

        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                fill=SNAKE_COLOR, tag="snake"
            )
            self.squares.append(square)


class Food:

    def __init__(self):

        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

            if [x, y] not in snake.coordinates:
                break

        self.coordinates = [x, y]

        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE,
            fill=FOOD_COLOR, tag="food"
        )


def drawGrid():
    for x in range(0, GAME_WIDTH, SPACE_SIZE):
        canvas.create_line(x, 0, x, GAME_HEIGHT, fill=GRID_COLOR)

    for y in range(0, GAME_HEIGHT, SPACE_SIZE):
        canvas.create_line(0, y, GAME_WIDTH, y, fill=GRID_COLOR)


def nextTurn():

    global score, SPEED, food

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake.coordinates.insert(0, [x, y])

    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE,
        fill=SNAKE_COLOR
    )

    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:

        score += 1
        label.config(text="Score: {}".format(score))

        canvas.delete("food")
        food = Food()

        if SPEED > 40:
            SPEED -= 5

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if checkCollisions():
        gameOver()
    else:
        window.after(SPEED, nextTurn)


def changeDirection(new_direction):

    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction

    elif new_direction == 'right' and direction != 'left':
        direction = new_direction

    elif new_direction == 'up' and direction != 'down':
        direction = new_direction

    elif new_direction == 'down' and direction != 'up':
        direction = new_direction


def checkCollisions():

    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True

    if y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False


def gameOver():

    canvas.delete(ALL)

    canvas.create_text(
        GAME_WIDTH/2,
        GAME_HEIGHT/2 - 40,
        font=('consolas', 50),
        text="GAME OVER",
        fill="red"
    )

    restart_button = Button(
        window,
        text="Restart",
        font=('consolas', 20),
        command=restartGame
    )

    canvas.create_window(GAME_WIDTH/2, GAME_HEIGHT/2 + 40, window=restart_button)


def restartGame():

    global snake, food, score, direction, SPEED

    canvas.delete(ALL)
    drawGrid()

    score = 0
    SPEED = 120
    direction = 'down'

    label.config(text="Score: 0")

    snake = Snake()
    food = Food()

    nextTurn()


window = Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = "down"

label = Label(window, text="Score: 0", font=('consolas', 35))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

drawGrid()

window.update()

window.bind('<Left>', lambda event: changeDirection('left'))
window.bind('<Right>', lambda event: changeDirection('right'))
window.bind('<Up>', lambda event: changeDirection('up'))
window.bind('<Down>', lambda event: changeDirection('down'))

snake = Snake()
food = Food()

nextTurn()

window.mainloop()