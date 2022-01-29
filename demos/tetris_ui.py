from demos.tetris import *
from de.scripts.simple_pg import *
from de.scripts.windows import *
from demos.color_manager import *

def draw_tetris_square(x, y, width, color):
    hsv_rep = hsv(color)
    highlight_color = rgb(hsv_rep[0], hsv_rep[1] * 0.3, hsv_rep[2] + (1 - hsv_rep[2]) * 0.3)
    shadow_color = rgb(hsv_rep[0], hsv_rep[1] * 0.8, hsv_rep[2] * 0.45)
    rectangle(x, y, width, width, shadow_color, surface=w1.surface)
    rectangle(x, y, width * 0.85, width * 0.85, color, surface=w1.surface)
    rectangle(x + width * 0.1, y + width * 0.1, width * 0.15, width * 0.6, highlight_color, surface=w1.surface)
    rectangle(x + width * 0.1, y + width * 0.1, width * 0.6, width * 0.15, highlight_color, surface=w1.surface)


def init():
    global game, time_until_drop, drop_speed, drop_accelerator, paused, w1

    game = Game(Vector2(10, 20))
    drop_speed = 0.3
    time_until_drop = drop_speed
    drop_accelerator = 1
    paused = False

    w1 = Window(events, np.array([400, 10]), np.array([350, 650]))

def events(event: pygame.event.Event):
    global game, time_until_drop, drop_speed, drop_accelerator, paused, w1
    if not paused:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                game.move_left()
            if event.key == pygame.K_RIGHT:
                game.move_right()
            if event.key == pygame.K_DOWN:
                drop_accelerator = 3
                time_until_drop -= drop_speed - drop_speed / drop_accelerator
            if event.key == pygame.K_UP:
                game.rotate_cw()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                drop_accelerator = 1
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            paused = not paused


def tick(delta):
    global game, time_until_drop, drop_speed, drop_accelerator, paused, w1

    if not paused:
        time_until_drop -= delta
        if time_until_drop < 0:
            game.move_down()
            time_until_drop = drop_speed / drop_accelerator
            rows_cleared = game.clear_full_rows()
            if rows_cleared > 0:
                print(rows_cleared)

def draw():
    global game, paused, w1
    fill((255, 255, 255), w1.surface)
    joined_array = game.get_full_array()
    rectangle(25, 25, 300, 600, tetr.color[0], surface=w1.surface)
    for x in range(len(joined_array)):
        for y in range(len(joined_array[x]) - 4):
            if joined_array[x][y + 4] != 0:
                draw_tetris_square(25 + x * 30, 25 + y * 30, 30, tetr.color[joined_array[x][y + 4]])
    if paused:
        rectangle(10, 10, 20, 50, (180, 180, 200), surface=w1.surface)
        rectangle(40, 10, 20, 50, (180, 180, 200), surface=w1.surface)
