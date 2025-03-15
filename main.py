import os
from random import randrange, random
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
background_blackalpha = pygame.image.load('sprites/background(alpha_black).png').convert_alpha()
background = pygame.image.load('sprites/greenhill_background.png').convert()

sonic_sprites_stay = {
    "W": pygame.image.load('sprites/sonic_sprites/W_keyboard/sonic_sprites_1_2.png').convert_alpha(),
    "S": pygame.image.load('sprites/sonic_sprites/S_keyboard/sonic_sprites_1_1.png').convert_alpha(),
    "A": pygame.image.load('sprites/sonic_sprites/A_keyboard/sonic_sprites_1_4.png').convert_alpha(),
    "D": pygame.image.load('sprites/sonic_sprites/D_keyboard/sonic_sprites_1_3.png').convert_alpha()
}

sonic_sprites = {
    "W": [pygame.image.load(f'sprites/sonic_sprites/W_keyboard/sonic_sprites_{i}.png').convert_alpha() for i in
          ['1_2', '2_3', '2_4']],
    "S": [pygame.image.load(f'sprites/sonic_sprites/S_keyboard/sonic_sprites_{i}.png').convert_alpha() for i in
          ['1_1', '2_1', '2_2']],
    "A": [pygame.image.load(f'sprites/sonic_sprites/A_keyboard/sonic_sprites_{i}.png').convert_alpha() for i in
          ['1_4', '2_7', '2_8']],
    "D": [pygame.image.load(f'sprites/sonic_sprites/D_keyboard/sonic_sprites_{i}.png').convert_alpha() for i in
          ['1_3', '2_5', '2_6']]
}

spindash_sprites = {
    "W": [pygame.image.load(f'sprites/spindash_sprites/W_keyboard/spindash_sprites_{i}.png').convert_alpha() for i in
          ['1_2', '2_3', '2_4']],
    "S": [pygame.image.load(f'sprites/spindash_sprites/S_keyboard/spindash_sprites_{i}.png').convert_alpha() for i in
          ['1_1', '2_1', '2_2']],
    "A": [pygame.image.load(f'sprites/spindash_sprites/A_keyboard/spindash_sprites_{i}.png').convert_alpha() for i in
          ['1_4', '2_7', '2_8']],
    "D": [pygame.image.load(f'sprites/spindash_sprites/D_keyboard/spindash_sprites_{i}.png').convert_alpha() for i in
          ['1_3', '2_5', '2_6']]
}


bomb_sprites = [pygame.image.load('sprites/bomb_sprites/bomb_sprites_1.png').convert_alpha(),
                pygame.image.load('sprites/bomb_sprites/bomb_sprites_2.png').convert_alpha()]


# Функция для создания новой игры
def new_game():
    global bomb_animation_index, bomb_animation_speed
    x, y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    ring = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    ring_box = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    spawn_ringbox = False
    spawn_bombs = False
    spindash = False
    press_e_key = 0
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    length = 1
    sonic = [(x, y)]
    dx, dy = 0, 0
    score = 0
    fps = 5
    current_sprite = sonic_sprites_stay["W"]
    animation_index = 0
    animation_speed = 1  # Чем выше число, тем медленнее смена кадров
    bomb_animation_index = 0
    bomb_animation_speed = 10
    return x, y, ring, ring_box, press_e_key, spawn_bombs, spindash, spawn_ringbox, dirs, length, sonic, dx, dy, score, fps, current_sprite, animation_index, animation_speed


# Функция для отображения кнопки рестарта
def draw_restart_button(screen):
    gameover = pygame.font.SysFont('soniclogojp', 70)
    restart_text = gameover.render("GAME OVER", 1, (208, 2, 27))
    screen.blit(background_blackalpha, (0, 0))
    screen.blit(restart_text, (140, 310))

    font = pygame.font.SysFont('soniclogojp', 36)
    restart_text = font.render('Press "R" to restart', 1, (255, 255, 255))
    screen.blit(restart_text, (135, 410))


# Переменные игры
x, y, ring, ring_box, spawn_ringbox, press_e_key, spindash, spawn_bombs, dirs, length, sonic, dx, dy, score, fps, current_sprite, animation_index, animation_speed = new_game()
game_over = False
current_direction = "W"  # Положение Соника при старте игры

# Главный цикл игры
while True:
    sc.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                x, y, ring, ring_box, press_e_key, spawn_ringbox, spawn_bombs, spindash, dirs, length, sonic, dx, dy, score, fps, current_sprite, animation_index, animation_speed = new_game()
                game_over = False

    if not game_over:
        # Управление
        keys = pygame.key.get_pressed()
        moving = False

        if keys[pygame.K_w] and dirs['W']:
            dx, dy = 0, -1
            current_direction = "W"
            moving = True
        if keys[pygame.K_s] and dirs['S']:
            dx, dy = 0, 1
            current_direction = "S"
            moving = True
        if keys[pygame.K_a] and dirs['A']:
            dx, dy = -1, 0
            current_direction = "A"
            moving = True
        if keys[pygame.K_d] and dirs['D']:
            dx, dy = 1, 0
            current_direction = "D"
            moving = True
        if keys[pygame.K_e]:
            if score >= 50:
                score -= 50
                fps = 5
        if keys[pygame.K_SPACE]:
            spindash = True
        else:
            spindash = False

        # Анимации
        if moving:
            animation_index += 1
            if animation_index >= animation_speed * len(sonic_sprites[current_direction]):
                animation_index = 0
            if spindash:
                current_sprite = spindash_sprites[current_direction][animation_index // animation_speed]
            else:
                current_sprite = sonic_sprites[current_direction][animation_index // animation_speed]
        else:
            current_sprite = sonic_sprites_stay[current_direction]
        # Отрисовка спрайтов
        sc.blit(current_sprite, (x, y))
        ring_img = pygame.image.load('sprites/ring.png').convert_alpha()
        ring_box_img = pygame.image.load('sprites/ring-box.png').convert_alpha()
        sc.blit(ring_img, ring)

        # Отображение количества колец
        font_score = pygame.font.SysFont('soniclogo_jp', 36)
        render_score = font_score.render(f"Rings: {score}", 1, (255, 215, 0))
        sc.blit(render_score, (5, 750))

        # Движение Соника
        x += dx * SIZE
        y += dy * SIZE
        sonic.append((x, y))
        sonic = sonic[-length:]

        # Перемещение на проивоположную сторону окна
        if x < 0:
            x = RES - SIZE
        elif x > RES - SIZE:
            x = 0
        if y < 0:
            y = RES - SIZE
        elif y > RES - SIZE:
            y = 0

        # Радиус, в котором кольцо подбирается
        COLLISION_RADIUS = SIZE // 1
        distance = math.sqrt((x - ring[0]) ** 2 + (y - ring[1]) ** 2)
        if distance < COLLISION_RADIUS:
            ring = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
            score += 1
            fps += 0.1

        # Проверка спавна мониторов с кольцами
        if score >= 5 and not spawn_ringbox:
            if random() < 0.03:
                spawn_ringbox = True
                ring_box = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
        if spawn_ringbox:
            sc.blit(ring_box_img, ring_box)
            COLLISION_RADIUS = SIZE // 1
            distance = math.sqrt((x - ring_box[0]) ** 2 + (y - ring_box[1]) ** 2)
            if distance < COLLISION_RADIUS and keys[pygame.K_SPACE]:
                spawn_ringbox = False
                score += 10
                fps += 0.5

        if score >= 5 and not spawn_ringbox:
            if random() < 0.07:
                spawn_bombs = True
                bomb = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
        if spawn_bombs:
            bomb_animation_index += 1
            if bomb_animation_index >= bomb_animation_speed * len(bomb_sprites):
                bomb_animation_index = 0
            current_bomb_sprite = bomb_sprites[bomb_animation_index // bomb_animation_speed]
            sc.blit(current_bomb_sprite, bomb)
            COLLISION_RADIUS = SIZE // 1
            distance = math.sqrt((x - bomb[0]) ** 2 + (y - bomb[1]) ** 2)
            if distance < COLLISION_RADIUS:
                spawn_bombs = False
                score -= 10
                fps -= 1
    if score < 0:
            game_over = True
    if game_over:
            draw_restart_button(sc)
            pygame.display.flip()
            continue

    pygame.display.flip()
    clock.tick(fps)
