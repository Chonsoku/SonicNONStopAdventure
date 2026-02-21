from random import randrange, random
import os, sys, time

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

import pygame
import math


RES = 800
SIZE = 55

pygame.init()
pygame.display.set_caption('Sonic NONStop Adventure')

icon = pygame.image.load(resource_path('assets/other/game_icon.png'))
pygame.display.set_icon(icon)

# Создание окна
sc = pygame.display.set_mode([RES, RES])
clock = pygame.time.Clock()
background_blackalpha = pygame.image.load(resource_path('assets/sprites/background(alpha_black).png')).convert_alpha()
background = pygame.image.load(resource_path('assets/sprites/greenhill_background.png')).convert()

sonic_sprites_stay = {
    "W": pygame.image.load(resource_path('assets/sprites/sonic_sprites/W_keyboard/sonic_sprites_1_2.png')).convert_alpha(),
    "S": pygame.image.load(resource_path('assets/sprites/sonic_sprites/S_keyboard/sonic_sprites_1_1.png')).convert_alpha(),
    "A": pygame.image.load(resource_path('assets/sprites/sonic_sprites/A_keyboard/sonic_sprites_1_4.png')).convert_alpha(),
    "D": pygame.image.load(resource_path('assets/sprites/sonic_sprites/D_keyboard/sonic_sprites_1_3.png')).convert_alpha()
}

sonic_sprites = {
    "W": [pygame.image.load(resource_path(f'assets/sprites/sonic_sprites/W_keyboard/sonic_sprites_{i}.png')).convert_alpha() for i in
          ['1_2', '2_3', '2_4']],
    "S": [pygame.image.load(resource_path(f'assets/sprites/sonic_sprites/S_keyboard/sonic_sprites_{i}.png')).convert_alpha() for i in
          ['1_1', '2_1', '2_2']],
    "A": [pygame.image.load(resource_path(f'assets/sprites/sonic_sprites/A_keyboard/sonic_sprites_{i}.png')).convert_alpha() for i in
          ['1_4', '2_7', '2_8']],
    "D": [pygame.image.load(resource_path(f'assets/sprites/sonic_sprites/D_keyboard/sonic_sprites_{i}.png')).convert_alpha() for i in
          ['1_3', '2_5', '2_6']]
}

spindash_sprites = {
    "W": [pygame.image.load(resource_path(f'assets/sprites/spindash_sprites/W_keyboard/spindash_sprites_{i}.png')).convert_alpha() for i in
          ['1_2', '2_3', '2_4']],
    "S": [pygame.image.load(resource_path(f'assets/sprites/spindash_sprites/S_keyboard/spindash_sprites_{i}.png')).convert_alpha() for i in
          ['1_1', '2_1', '2_2']],
    "A": [pygame.image.load(resource_path(f'assets/sprites/spindash_sprites/A_keyboard/spindash_sprites_{i}.png')).convert_alpha() for i in
          ['1_4', '2_7', '2_8']],
    "D": [pygame.image.load(resource_path(f'assets/sprites/spindash_sprites/D_keyboard/spindash_sprites_{i}.png')).convert_alpha() for i in
          ['1_3', '2_5', '2_6']]
}

badnikbug_sprites_x = {
    "left": [pygame.image.load(resource_path(f'assets/sprites/badnikbug_sprites/axis X/badnikbug_sprites_{i}.png')).convert_alpha() for i in
             ['1(left)', '2(left)', '3(left)', '4(left)']],
    "right": [pygame.image.load(resource_path(f'assets/sprites/badnikbug_sprites/axis X/badnikbug_sprites_{i}.png')).convert_alpha() for i in
              ['1(right)', '2(right)', '3(right)', '4(right)']]
}

badnikbug_sprites_y = {
    "up": [pygame.image.load(resource_path(f'assets/sprites/badnikbug_sprites/axis Y/badnikbug_sprites_{i}.png')).convert_alpha() for i in
             ['1(up)', '2(up)', '3(up)', '4(up)']],
    "down": [pygame.image.load(resource_path(f'assets/sprites/badnikbug_sprites/axis Y/badnikbug_sprites_{i}.png')).convert_alpha() for i in
              ['1(down)', '2(down)', '3(down)', '4(down)']]
}


bomb_sprites = [pygame.image.load(resource_path('assets/sprites/bomb_sprites/bomb_sprites_1.png')).convert_alpha(),
                pygame.image.load(resource_path('assets/sprites/bomb_sprites/bomb_sprites_2.png')).convert_alpha()]

sprite_press_e = pygame.image.load(resource_path('assets/sprites/sprite_press_e.png')).convert_alpha()


# Функция для создания новой игры
def new_game():
    x, y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    ring = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    ring_box = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
    spawn_ringbox = False
    spawn_bombs = False
    spawn_badniksbugs_x = False
    spawn_badniksbugs_y = False
    spindash_active = False
    press_e_key = 0
    dirs = {'W': True, 'S': True, 'A': True, 'D': True}
    sonic = [(x, y)]
    dx, dy = 0, 0
    number_rings = 0
    fps = 30

    current_sprite = sonic_sprites_stay["W"]
    animation_index = 0
    animation_speed = 5  # Чем выше число, тем медленнее смена кадров

    return x, y, ring, ring_box, press_e_key, spawn_bombs, spindash_active, spawn_badniksbugs_x, spawn_badniksbugs_y, spawn_ringbox, dirs, sonic, dx, dy, number_rings, fps, current_sprite, animation_index, animation_speed


# Функция для отображения кнопки рестарта
def draw_restart_button(screen):
    gameover = pygame.font.SysFont('Sonic Logo-JP', 70)
    restart_text = gameover.render("GAME OVER", 1, (208, 2, 27))
    screen.blit(background_blackalpha, (0, 0))
    screen.blit(restart_text, (140, 310))

    font = pygame.font.SysFont('Sonic Logo-JP', 36)
    restart_text = font.render('Press "R" to restart', 1, (255, 255, 255))
    screen.blit(restart_text, (135, 410))


# Переменные игры
x, y, ring, ring_box, spawn_ringbox, press_e_key, spawn_badniksbugs_x, spawn_badniksbugs_y, spindash_active, spawn_bombs, dirs, sonic, dx, dy, number_rings, fps, current_sprite, animation_index, animation_speed = new_game()
game_over = False
speed = 5
bomb_animation_index = 0
bomb_animation_speed = 10
bomb_spawn_time = 0  # Время, когда бомбы были созданы
bomb_duration = 5  # Время жизни бомб в секундах
badnikbug_animation_index_x = 0
badnikbug_animation_speed_x = 2
badnikbug_direction_x = "left"
badnikbug_speed_x = 5
badnikbug_animation_index_y = 0
badnikbug_animation_speed_y = 2
badnikbug_direction_y = "up"
badnikbug_speed_y = 5  # Скорость движения бадника
spindash_start_time = 0
spindash_duration = 2  # Длительность спиндеша в секундах
spindash_cooldown = 1.5  # Время перезарядки в секундах
spindash_cooldown_start = 0
spindash_on_cooldown = False
invulnerability_time = 1  # Время, когда игрок стал уязвимым
invulnerability_duration = 1.5  # Длительность уязвимости в секундах
is_invulnerable = False
current_direction = "W"

# Главный цикл игры
while True:
    sc.blit(background, (0, 0))
    current_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                x, y, ring, ring_box, press_e_key, spawn_ringbox, spawn_badniksbugs_x, spawn_badniksbugs_y, spawn_bombs, spindash_active, dirs, sonic, dx, dy, number_rings, fps, current_sprite, animation_index, animation_speed = new_game()
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
            if number_rings >= 50:
                press_e_key = 1
                number_rings -= 50
                speed = 5
        if keys[pygame.K_SPACE] and not spindash_on_cooldown:
            if not spindash_active:
                spindash_active = True
                speed += 2.5
                spindash_start_time = current_time
        if spindash_active:
            if current_time - spindash_start_time >= spindash_duration:
                spindash_active = False
                speed -= 2.5
                spindash_on_cooldown = True
                spindash_cooldown_start = current_time
        if spindash_on_cooldown:
            if current_time - spindash_cooldown_start >= spindash_cooldown:
                spindash_on_cooldown = False

        # Отрисовка спрайтов
        sc.blit(current_sprite, (x, y))
        ring_img = pygame.image.load(resource_path('assets/sprites/ring.png')).convert_alpha()
        ring_box_img = pygame.image.load(resource_path('assets/sprites/ring-box.png')).convert_alpha()
        sc.blit(ring_img, ring)

        # Движение Соника
        x += dx * speed
        y += dy * speed
        sonic.append((x, y))

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
        COLLISION_RADIUS = SIZE * 1.2
        distance = math.sqrt((x - ring[0]) ** 2 + (y - ring[1]) ** 2)
        if distance < COLLISION_RADIUS:
            ring = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
            number_rings += 1
            speed += 0.1

        # Проверка спавна мониторов с кольцами
        if number_rings >= 5 and not spawn_ringbox:
            if random() < 0.03:
                spawn_ringbox = True
                ring_box = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
        if spawn_ringbox:
            sc.blit(ring_box_img, ring_box)
            COLLISION_RADIUS = SIZE * 1.5
            distance = math.sqrt((x - ring_box[0]) ** 2 + (y - ring_box[1]) ** 2)
            if distance < COLLISION_RADIUS and spindash_active:
                spawn_ringbox = False
                number_rings += 10
                speed += 0.5

        # Проверка спавна бомб
        if number_rings >= 10 and not spawn_bombs:
            if random() < 0.05:
                spawn_bombs = True
                bomb = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
                bomb_spawn_time = time.time()
        if spawn_bombs:
            if time.time() - bomb_spawn_time >= bomb_duration:
                spawn_bombs = False
                bomb_spawn_time = time.time()
            bomb_animation_index += 1
            if bomb_animation_index >= bomb_animation_speed * len(bomb_sprites):
                bomb_animation_index = 0
            current_bomb_sprite = bomb_sprites[bomb_animation_index // bomb_animation_speed]
            sc.blit(current_bomb_sprite, bomb)
            COLLISION_RADIUS = SIZE * 1.5
            distance = math.sqrt((x - bomb[0]) ** 2 + (y - bomb[1]) ** 2)
            if distance < COLLISION_RADIUS:
                if not is_invulnerable:  # Если игрок неуязвим
                    spawn_bombs = False
                    is_invulnerable = True
                    invulnerability_time = time.time()  # Запомнить время активации уязвимости
                    number_rings -= 20
                    speed -= 20
                    # Игрок уязвим - потом добавить эффект мерцание
            # Обработка времени уязвимости
            if is_invulnerable:
                if time.time() - invulnerability_time >= invulnerability_duration:
                    is_invulnerable = False
            if speed <= 5:
                speed = 5

        # Переменные для бадника-жука по оси X
        if number_rings >= 30 and not spawn_badniksbugs_x:
            if random() < 0.5:
                spawn_badniksbugs_x = True
                badnikbug_x = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
                badnikbug_direction_x = "left" if random() < 0.5 else "right"
        if spawn_badniksbugs_x:
            if badnikbug_direction_x == "left":
                badnikbug_x = (badnikbug_x[0] - badnikbug_speed_x, badnikbug_x[1])  # Обновляем координаты X
                if badnikbug_x[0] < 0:  # Если выходит за пределы экрана, меняем направление
                    badnikbug_direction_x = "right"
            else:
                badnikbug_x = (badnikbug_x[0] + badnikbug_speed_x, badnikbug_x[1])  # Обновляем координаты X
                if badnikbug_x[0] > RES - SIZE:  # Если выходит за пределы экрана, меняем направление
                    badnikbug_direction_x = "left"
            # Обновление индекса анимации
            badnikbug_animation_index_x += 1
            if badnikbug_animation_index_x >= badnikbug_animation_speed_x * len(badnikbug_sprites_x[badnikbug_direction_x]):
                badnikbug_animation_index_x = 0
            current_badnik_sprite_x = badnikbug_sprites_x[badnikbug_direction_x][
                badnikbug_animation_index_x // badnikbug_animation_speed_x]
            sc.blit(current_badnik_sprite_x, badnikbug_x)  # Отображаем бадника
            COLLISION_RADIUS = SIZE * 1.5
            distance = math.sqrt((x - badnikbug_x[0]) ** 2 + (y - badnikbug_x[1]) ** 2)
            if distance < COLLISION_RADIUS and spindash_active:
                spawn_badniksbugs_x = False
            elif distance < COLLISION_RADIUS:
                if not is_invulnerable:  # Если игрок неуязвим
                    is_invulnerable = True
                    invulnerability_time = time.time()  # Запомнить время активации уязвимости
                    number_rings -= 20
                    speed -= 20
                    # Игрок уязвим - потом добавить эффект мерцания
        # Обработка времени уязвимости
        if is_invulnerable:
            if time.time() - invulnerability_time >= invulnerability_duration:
                is_invulnerable = False
        if speed <= 5:
            speed = 5

            # Переменные для бадника-жука по оси Y
            if number_rings >= 30 and not spawn_badniksbugs_y:
                if random() < 0.5:
                    spawn_badniksbugs_y = True
                    badnikbug_y = randrange(0, RES - SIZE, SIZE), randrange(0, RES - SIZE, SIZE)
                    badnikbug_direction_y = "up" if random() < 0.5 else "down"
            if spawn_badniksbugs_y:
                if badnikbug_direction_y == "up":
                    badnikbug_y = (badnikbug_y[0], badnikbug_y[1] - badnikbug_speed_y)  # Изменяем Y координату
                    if badnikbug_y[1] < 0:  # Если выходит за пределы экрана, меняем направление
                        badnikbug_direction_y = "down"
                else:
                    badnikbug_y = (badnikbug_y[0], badnikbug_y[1] + badnikbug_speed_y)  # Изменяем Y координату
                    if badnikbug_y[1] > RES - SIZE:  # Если выходит за пределы экрана, меняем направление
                        badnikbug_direction_y = "up"
                badnikbug_animation_index_y += 1
                if badnikbug_animation_index_y >= badnikbug_animation_speed_y * len(
                        badnikbug_sprites_y[badnikbug_direction_y]):
                    badnikbug_animation_index_y = 0
                current_badnik_sprite_y = badnikbug_sprites_y[badnikbug_direction_y][
                    badnikbug_animation_index_y // badnikbug_animation_speed_y]
                sc.blit(current_badnik_sprite_y, badnikbug_y)                                # Пока что, конкретно бадник-жук по оси Y - работает не корректно.
                COLLISION_RADIUS = SIZE * 1.5                                                # Так как он уничтожается после нажатия кнопки спиндеша, игнорируя проверку коллизии!
                distance = math.sqrt((x - badnikbug_y[0]) ** 2 + (y - badnikbug_y[1]) ** 2)
                if distance < COLLISION_RADIUS and spindash_active:
                    spawn_badniksbugs_x = False
                elif distance < COLLISION_RADIUS:
                    if not is_invulnerable:  # Если игрок неуязвим
                        is_invulnerable = True
                        invulnerability_time = time.time()  # Запомнить время активации уязвимости
                        number_rings -= 20
                        speed -= 20
                        # Игрок уязвим - потом добавить эффект мерцания
            # Обработка времени уязвимости
            if is_invulnerable:
                if time.time() - invulnerability_time >= invulnerability_duration:
                    is_invulnerable = False
            if speed <= 5:
                speed = 5

        # Анимации
        if moving:
            animation_index += 1
            if animation_index >= animation_speed * len(sonic_sprites[current_direction]):
                animation_index = 0
            if spindash_active:
                current_sprite = spindash_sprites[current_direction][animation_index // animation_speed]
            else:
                current_sprite = sonic_sprites[current_direction][animation_index // animation_speed]
        else:
            current_sprite = sonic_sprites_stay[current_direction]

        # Отрисовка кнопки "press_e"
        if number_rings >= 50:
            sc.blit(sprite_press_e, (615, 720))
        # Отображение количества колец
        font_ring_number = pygame.font.SysFont('Sonic Logo-JP', 36)
        render_ring_number = font_ring_number.render(f"Rings: {number_rings}", 1, (255, 215, 0))
        sc.blit(render_ring_number, (5, 750))

    # Проверка на Game Over
    if number_rings < 0:
            game_over = True
    if game_over:
            draw_restart_button(sc)
            pygame.display.flip()
            continue

    pygame.display.flip()
    clock.tick(fps)
