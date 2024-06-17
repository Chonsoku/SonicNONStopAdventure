import os
from random import randrange

import pygame
from pygame import surface

RES = 800
SIZE = 55
pygame.font.init()

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

pygame.init()
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
background = pygame.image.load('greenhill(background).png').convert()
game_over = False

x, y, ring, dirs, length, sonic, dx, dy, score, fps = new_game()

while True:
    sc.blit(background, (0, 0))

    if not game_over:
        # Отрисовка змейки и яблок
        [(pygame.draw.rect(sc, pygame.Color('green'), (i, j, SIZE - 3, SIZE - 3))) for i, j in sonic]
        imgSize = (65, 65)
        ring_image = pygame.image.load('ring.png').convert_alpha()
        sc.blit(ring_image, (ring))
        # Рендер надписи колец
        font_score = pygame.font.SysFont('soniclogojp', 36)
        render_score = font_score.render("Rings: " + str(score), 1, (255, 215, 0))
        # Движение змейки
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
        key = pygame.key.get_pressed()
        if key[pygame.K_w] and dirs['W']:
            dx, dy = 0, -1
            dirs = {'W': True, 'S': True, 'A': True, 'D': True}
        if key[pygame.K_s] and dirs['S']:
            dx, dy = 0, 1
            dirs = {'W': True, 'S': True, 'A': True, 'D': True}
        if key[pygame.K_a] and dirs['A']:
            dx, dy = -1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': True}
        if key[pygame.K_d] and dirs['D']:
            dx, dy = 1, 0
            dirs = {'W': True, 'S': True, 'A': True, 'D': True}
            pygame.event.get()

        # Смерть
        if x < 0 or x > RES - SIZE or y < 0 or y > RES - SIZE or len(sonic) != len(set(sonic)):
            game_over = True

    else:
        draw_restart_button(sc)

    pygame.display.flip()
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                x, y, apple, dirs, length, snake, dx, dy, score, fps = new_game()
                game_over = False
