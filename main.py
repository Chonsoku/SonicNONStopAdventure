import os
from random import randrange
import pygame

RES = 800
SIZE = 55

pygame.init()
pygame.display.set_caption('Sonic NONStop Adventure')

icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

# Создаём окно
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
background = pygame.image.load('sprites/greenhill_background.png').convert()


# Функция для создания новой игры
def new_game():
    x, y = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    ring = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    length = 1
    sonic = [(x, y)]
    dx, dy = 0, 0
    score = 0
    fps = 5
    return x, y, ring, dirs, length, sonic, dx, dy, score, fps


# Функция для отображения кнопки рестарта
def draw_restart_button(screen):
    gameover = pygame.font.SysFont('soniclogojp', 70)
    restart_text = gameover.render("GAME OVER", 1, (208, 2, 27))
    screen.blit(restart_text, (140, 310))

    font = pygame.font.SysFont('soniclogojp', 36)
    restart_text = font.render('Press "R" to restart', 1, (255, 255, 255))
    screen.blit(restart_text, (135, 410))


# Переменные игры
x, y, ring, dirs, length, sonic, dx, dy, score, fps = new_game()
game_over = False

# Главный цикл игры
while True:
    sc.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                x, y, ring, dirs, length, sonic, dx, dy, score, fps = new_game()
                game_over = False

    if not game_over:
        # Отрисовка персонажа и колец
        sonic_img = pygame.image.load('sprites/sonic_sprites_1_2.png').convert_alpha()
        ring_img = pygame.image.load('sprites/ring.png').convert_alpha()

        sc.blit(sonic_img, (x, y))
        sc.blit(ring_img, ring)

        # Отображение количества колец
        font_score = pygame.font.SysFont('soniclogo_jp', 36)
        render_score = font_score.render(f"Rings: {score}", 1, (255, 215, 0))
        sc.blit(render_score, (5, 750))

        # Движение соника
        x += dx * SIZE
        y += dy * SIZE
        sonic.append((x, y))
        sonic = sonic[-length:]

        # Подбирание колец
        if sonic[-1] == ring:
            ring = randrange(0, RES, SIZE), randrange(0, RES, SIZE)
            score += 1
            fps += 1

        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dirs['W']:
            dx, dy = 0, -1
        if keys[pygame.K_s] and dirs['S']:
            dx, dy = 0, 1
        if keys[pygame.K_a] and dirs['A']:
            dx, dy = -1, 0
        if keys[pygame.K_d] and dirs['D']:
            dx, dy = 1, 0

        # Проверка на столкновение (границы экрана или хвост)
        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(sonic) != len(set(sonic)):
            game_over = True

    else:
        draw_restart_button(sc)

    pygame.display.flip()
    clock.tick(fps)
