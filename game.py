import tkinter
import random

# Constants
WIDTH = 640
HEIGHT = 480
BG_COLOR = 'white'
MAIN_BALL_RADIUS = 30
MAIN_BALL_COLOR = 'blue'
INIT_DX = 2
INIT_DY = 2
DELAY = 20
EVIL_BALL_COLOR = 'red'
EVIL_BALL_OUTLINE_COLOR = 'black'
COLORS = ['black', 'yellow', 'green', EVIL_BALL_COLOR, 'orange']

evil_balls_count = 0


# Ball class
class Balls():
    def __init__(self, x, y, r, c, dx = 0, dy = 0):
        self.x = x
        self.y = y
        self.r = r
        self.c = c
        self.dx = dx
        self.dy = dy

    def draw(self):
        canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill = self.c,
            outline = self.c if self.c != EVIL_BALL_COLOR else EVIL_BALL_OUTLINE_COLOR
        )
    
    def hide(self):
        canvas.create_oval(
            self.x - self.r,
            self.y - self.r,
            self.x + self.r,
            self.y + self.r,
            fill = BG_COLOR,
            outline = BG_COLOR
        )
    
    def is_collision(self, ball):
        a = abs(self.x + self.dx - ball.x)
        b = abs(self.y + self.dy - ball.y)
        return (a * a + b * b) ** 0.5 <= self.r + ball.r

    def move(self):
        # collide with walls
        if (self.x + self.r + self.dx >= WIDTH) or (self.x - self.r + self.dx <= 0):
            self.dx = -self.dx
        if (self.y + self.r + self.dy >= HEIGHT) or (self.y - self.r + self.dy <= 0):
            self.dy  = -self.dy
        for ball in balls:
            if self.is_collision(ball):
                if ball.c != EVIL_BALL_COLOR:
                    ball.hide()
                    balls.remove(ball)
                    print(self.dx, self.dy)
                    # self.dx = -self.dx
                    # self.dy = -self.dy
                    self.dx = -(self.dx + 1 * random.random())
                    self.dy = -(self.dy + 1 * random.random())
                else:
                    self.dx = self.dy = 0
        self.hide()
        self.x += self.dx
        self.y += self.dy
        self.draw()


# mouse events
def mouse_click(event):
    global main_ball
    # print(event.num, event.x,  event.y)
    if event.num == 1:
        if 'main_ball' not in globals():
            main_ball = Balls(
                event.x,
                event.y,
                MAIN_BALL_RADIUS,
                MAIN_BALL_COLOR,
                INIT_DX,
                INIT_DY
            )
            main_ball.draw()
        else:
            if main_ball.dx * main_ball.dy > 0:
                main_ball.dy = -main_ball.dy
            else:
                main_ball.dx = -main_ball.dx
    elif event.num == 3:
        if main_ball.dx * main_ball.dy > 0:
            main_ball.dx = -main_ball.dx
        else:
            main_ball.dy = -main_ball.dy
        main_ball.hide()

def create_balls(number):
    global evil_balls_count
    lst = []
    while len(lst) < number:
        next_ball = Balls(random.choice(range(0, WIDTH)),
            random.choice(range(0, HEIGHT)),
            random.choice(range(15, 35)),
            random.choice(COLORS)
        )
        if next_ball.c == EVIL_BALL_COLOR:
            evil_balls_count += 1
        lst.append(next_ball)
        next_ball.draw()
    return lst

def count_bad_balls(balls):
    result = 0
    for ball in balls:
        if ball.c == EVIL_BALL_COLOR:
            result += 1
    return result

# main game cycle
def main():
    if 'main_ball' in globals():
        main_ball.move()
        if len(balls) - evil_balls_count == 0:
            canvas.create_text(
                WIDTH / 2, 
                HEIGHT / 2,
                text = 'You win',
                font = 'Arial',
                fill = MAIN_BALL_COLOR)
            main_ball.dx = main_ball.dy = 0
        elif main_ball.dx == 0:
            canvas.create_text(
                WIDTH / 2, 
                HEIGHT / 2,
                text = 'You loose',
                font = 'Arial',
                fill = EVIL_BALL_COLOR)
    root.after(DELAY, main)

root = tkinter.Tk()
root.title('Colliding Balls')
canvas = tkinter.Canvas(root, width = WIDTH, height = HEIGHT, bg = BG_COLOR)
canvas.pack()
# capture keyboard input - bind() method
canvas.bind('<Button-1>', mouse_click)
canvas.bind('<Button-2>', mouse_click, '+')
canvas.bind('<Button-3>', mouse_click, '*')
# if main_ball in globals:
#     del main_ball
balls = create_balls(7)
main()
root.mainloop()