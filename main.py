import os
from random import randrange
import pygame
import math


RES = 800
SIZE = 55

pygame.init()
pygame.display.set_caption('Sonic NONStop Adventure')

icon = pygame.image.load('game_icon.png')
pygame.display.set_icon(icon)

# Создание окна
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
background = pygame.image.load('sprites/greenhill_background.png').convert()

# Загрузка спрайтов Соника
sonic_sprites = {
    "W": pygame.image.load('sprites/sonic_sprites_1_2.png').convert_alpha(),
    "S": pygame.image.load('sprites/sonic_sprites_1_1.png').convert_alpha(),
    "A": pygame.image.load('sprites/sonic_sprites_1_4.png').convert_alpha(),
    "D": pygame.image.load('sprites/sonic_sprites_1_3.png').convert_alpha()
}

# Функция для создания новой игры
def new_game():
    x, y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    ring = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    length = 1
    sonic = [(x, y)]
    dx, dy = 0, 0
    score = 0
    fps = 5
    current_sprite = sonic_sprites["D"]
    return x, y, ring, dirs, length, sonic, dx, dy, score, fps, current_sprite


# Функция для отображения кнопки рестарта
def draw_restart_button(screen):
    gameover = pygame.font.SysFont('soniclogojp', 70)
    restart_text = gameover.render("GAME OVER", 1, (208, 2, 27))
    screen.blit(restart_text, (140, 310))

    font = pygame.font.SysFont('soniclogojp', 36)
    restart_text = font.render('Press "R" to restart', 1, (255, 255, 255))
    screen.blit(restart_text, (135, 410))

# Переменные игры
x, y, ring, dirs, length, sonic, dx, dy, score, fps, current_sprite = new_game()
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
                x, y, ring, dirs, length, sonic, dx, dy, score, fps, current_sprite = new_game()
                game_over = False

    if not game_over:
        # Управление
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and dirs['W']:
            dx, dy = 0, -1
            current_sprite = sonic_sprites["W"]
        if keys[pygame.K_s] and dirs['S']:
            dx, dy = 0, 1
            current_sprite = sonic_sprites["S"]
        if keys[pygame.K_a] and dirs['A']:
            dx, dy = -1, 0
            current_sprite = sonic_sprites["A"]
        if keys[pygame.K_d] and dirs['D']:
            dx, dy = 1, 0
            current_sprite = sonic_sprites["D"]

        # Отрисовка Соника
        sc.blit(current_sprite, (x, y))

        # Отрисовка колец
        ring_img = pygame.image.load('sprites/ring.png').convert_alpha()
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

        # Зацикливание экрана (перемещение на противоположную сторону)
        if x < 0:
            x = RES - SIZE
        elif x > RES - SIZE:
            x = 0
        if y < 0:
            y = RES - SIZE
        elif y > RES - SIZE:
            y = 0

        COLLISION_RADIUS = SIZE * 1  # Радиус, в котором кольцо подбирается
        # Подбирание колец
        distance = math.sqrt((x - ring[0]) ** 2 + (y - ring[1]) ** 2)
        if distance < COLLISION_RADIUS:
            ring = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
            score += 1
            fps += 0.1

    else:
        draw_restart_button(sc)

    pygame.display.flip()
    clock.tick(fps)
