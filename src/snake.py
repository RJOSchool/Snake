import random, pygame, sys
from pygame.locals import *

FPS = 15
WINDOW_WIDTH : int = 640
WINDOW_HEIGHT : int = 480
CELL_SIZE : int = 20
CELL_WIDTH : int = int(WINDOW_WIDTH / CELL_SIZE)
CELL_HEIGHT : int = int(WINDOW_HEIGHT / CELL_SIZE)

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)

UP : str= 'up'
DOWN : str= 'down'
LEFT : str = 'left'
RIGHT : str = 'right'
HEAD : int = 0

def main():
    global FPS_CLOCK, DISPLAY_SURF, FONT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FONT = pygame.font.Font('src/dlxfont.ttf', 12)
    pygame.display.set_caption('Snake')

    show_start_screen()
    while True:
        run_game()
        show_game_over_screen()

def run_game():
    x = 12
    y = 12
    coordinates = [{'x': x, 'y': y}, {'x': x - 1, 'y': y}, {'x': x - 2, 'y': y}]
    direction = RIGHT
    food = generate_position()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        if (coordinates[HEAD]['x'] == -1 or coordinates[HEAD]['x'] == CELL_WIDTH or
            coordinates[HEAD]['y'] == -1 or coordinates[HEAD]['y'] == CELL_HEIGHT):
            return  # Snake hit the wall, end game

        # Check if snake hit itself
        for segment in coordinates[1:]:
            if segment['x'] == coordinates[HEAD]['x'] and segment['y'] == coordinates[HEAD]['y']:
                return

        if coordinates[HEAD]['x'] == food['x'] and coordinates[HEAD]['y'] == food['y']:
            eat_sound = pygame.mixer.Sound('src/som_comida.wav')
            eat_sound.play()
            food = generate_position()
        else:
            del coordinates[-1]  # Remove tail segment

        # Move snake head
        if direction == UP:
            new_head = {'x': coordinates[HEAD]['x'], 'y': coordinates[HEAD]['y'] - 1}
        elif direction == DOWN:
            new_head = {'x': coordinates[HEAD]['x'], 'y': coordinates[HEAD]['y'] + 1}
        elif direction == LEFT:
            new_head = {'x': coordinates[HEAD]['x'] - 1, 'y': coordinates[HEAD]['y']}
        elif direction == RIGHT:
            new_head = {'x': coordinates[HEAD]['x'] + 1, 'y': coordinates[HEAD]['y']}

        coordinates.insert(0, new_head)
        DISPLAY_SURF.fill(BACKGROUND_COLOR)
        draw_snake(coordinates)
        draw_food(food)
        draw_score(len(coordinates) - 3)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

def draw_snake(coords):
    for c in coords:
        x = c['x'] * CELL_SIZE
        y = c['y'] * CELL_SIZE
        snake_segment = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(DISPLAY_SURF, GREEN, snake_segment)

def draw_food(c):
    x = c['x'] * CELL_SIZE
    y = c['y'] * CELL_SIZE
    food_rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(DISPLAY_SURF, RED, food_rect)

def draw_score(score):
    score_surf = FONT.render('Score: %s' % score, True, WHITE)
    score_rect = score_surf.get_rect()
    score_rect.topleft = (WINDOW_WIDTH - 625, 450)
    DISPLAY_SURF.blit(score_surf, score_rect)

def terminate():
    pygame.quit()
    sys.exit()

def generate_position():
    return {'x': random.randint(0, CELL_WIDTH - 1), 'y': random.randint(0, CELL_HEIGHT - 1)}

def show_start_screen():
    img = pygame.image.load('src/tela_inicial.png')
    img_x = 165
    img_y = 100

    while True:
        draw_instructions()

        if key_pressed():
            pygame.event.get()
            return
        pygame.display.update()
        DISPLAY_SURF.blit(img, (img_x, img_y))
        FPS_CLOCK.tick(FPS)

def draw_instructions():
    draw_text('Press any key to play', WINDOW_WIDTH / 2, 275)
    draw_text('Press Esc to quit', WINDOW_WIDTH / 2, 300)
    draw_text('2016 - Cristian Henrique', WINDOW_WIDTH / 2, 430)

def draw_text(text, x, y):
    text_obj = FONT.render(text, True, WHITE)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    DISPLAY_SURF.blit(text_obj, text_rect)

def key_pressed():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    key_up_events = pygame.event.get(KEYUP)
    if len(key_up_events) == 0:
        return None
    if key_up_events[0].key == K_ESCAPE:
        terminate()
    return key_up_events[0].key

def show_game_over_screen():
    game_over_font = pygame.font.Font('src/dlxfont.ttf', 45)
    game_over_surf = game_over_font.render('Game Over!', True, WHITE)
    game_over_rect = game_over_surf.get_rect()
    game_over_rect.midtop = (330, 50)

    DISPLAY_SURF.blit(game_over_surf, game_over_rect)
    draw_instructions()
    pygame.display.update()
    pygame.time.wait(500)
    key_pressed()

    while True:
        if key_pressed():
            pygame.event.get()
            return

main()
