import pygame
import time
from sys import exit

# Init
pygame.init()


def drawText(text, x, y, color, type_text):
    if type_text == "end":
        text = font_end.render(text, True, color)
        text_rect = text.get_rect(topleft=(x, y))
    else:
        text = font.render(text, True, color)
        text_rect = text.get_rect(topleft=(x, y))

    screen.blit(text, text_rect)


def playerAnimation(movement, Y_collision):
    global character_surf, character_index

    if Y_collision == False and movement:
        character_surf = character_jump
    elif Y_collision == False:
        character_surf = character_jump_stand
    else:
        if movement:
            character_index += 0.1
            if character_index >= len(character_walk):
                character_index = 0
            character_surf = character_walk[int(character_index)]
        else:
            character_surf = character_stand


def enemyAnimation():
    global enemy_surf, enemy_index

    enemy_index += 0.05
    if enemy_index >= len(enemy_walk):
        enemy_index = 0
    enemy_surf = enemy_walk[int(enemy_index)]

def timer():
    count = 0
    while count < 100000:
        count += 0.1


screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("O Jogo")
clock = pygame.time.Clock()

# Menu
play_rect = pygame.Rect(325, 40, 160, 75)

inst_rect = pygame.Rect(325, 125, 160, 75)
instruction = False

exit_rect = pygame.Rect(325, 210, 160, 75)
back_rect = pygame.Rect(325, 290, 160, 75)

menu_rect = pygame.Rect(325, 290, 160, 75)

# Music/Sounds
backgroun_music = pygame.mixer.music.load("sounds/pymusic.mp3")
pygame.mixer.music.play(-1)

live_up = pygame.mixer.Sound("sounds/live_up.wav")
collect_gun = pygame.mixer.Sound("sounds/gun_collect.wav")
enemy_hit = pygame.mixer.Sound("sounds/enemy_hit.wav")
shot_hit = pygame.mixer.Sound("sounds/shot_hit.wav")
shot = pygame.mixer.Sound("sounds/shot.wav")

music_on = True
music1 = pygame.image.load("sounds/sound_on.png")
music2 = pygame.image.load("sounds/sound_off.png")
music_rect = pygame.Rect(740, 320, 40, 40)

# Fonts
font = pygame.font.Font("font/Pixeltype.ttf", 35)

font_end = pygame.font.Font("font/Pixeltype.ttf", 65)

# BackGround
bg = pygame.image.load("graphics/sprites/night_0.png")

# Platforms
scene = [
    pygame.Rect(0, 380, 400, 20),
    pygame.Rect(400, 300, 400, 100),
    pygame.Rect(0, 215, 340, 20),
    pygame.Rect(0, 65, 340, 20),
    pygame.Rect(420, 140, 380, 20),
]

ground_0 = pygame.image.load("graphics/Ground/ground_0.png")
ground_1 = pygame.image.load("graphics/Ground/ground_1.png")
ground_2 = pygame.image.load("graphics/Ground/ground_2.png")
ground_3 = pygame.image.load("graphics/Ground/ground_3.png")

# Player
character_stand = pygame.image.load("graphics/sprites/sprite_00.png").convert_alpha()

character_walk1 = pygame.image.load("graphics/sprites/sprite_02c.png").convert_alpha()
character_walk2 = pygame.image.load("graphics/sprites/sprite_03c.png").convert_alpha()
character_walk3 = pygame.image.load("graphics/sprites/sprite_04c.png").convert_alpha()
character_walk = [character_walk1, character_walk2, character_walk3]
character_index = 0
character_jump = pygame.image.load("graphics/sprites/sprite_12c.png").convert_alpha()
character_jump_stand = pygame.image.load(
    "graphics/sprites/sprite_06c.png"
).convert_alpha()

character_surf = character_walk[character_index]

character_posX = 40
character_posY = 340

character_speed = 0
character_aceleration = 0.2

character_heigth = 34
character_width = 26

character_direction = "Right"

Y_collision = False

# Gun
gun_image = pygame.image.load("graphics/sprites/guns_4.png")
gun = [pygame.Rect(30, 45, 28, 15)]
guns = 1

laser_image = pygame.image.load("graphics/sprites/laser.png")
triggered = False

# Lives
lives = 3
heart_image = pygame.image.load("graphics/sprites/heart.png")

extra_life = [pygame.Rect(300, 25, 40, 40)]

# Enemys
enemy_walk1 = pygame.image.load(
    "graphics/sprite_enemy/slime_enemy_0c.png"
).convert_alpha()
enemy_walk2 = pygame.image.load(
    "graphics/sprite_enemy/slime_enemy_2c.png"
).convert_alpha()
enemy_walk3 = pygame.image.load(
    "graphics/sprite_enemy/slime_enemy_2_0c.png"
).convert_alpha()

enemy_walk = [enemy_walk1, enemy_walk2, enemy_walk3]
enemy_index = 0

enemy_surf = enemy_walk[enemy_index]

enemy_height = 34
enemy_width = 25

enemy_direction1 = "Left"
enemy_pos1X = 700
enemy_pos1Y = 267
enemy1_live = True

enemy_direction2 = "Left"
enemy_pos2X = 10
enemy_pos2Y = 182
enemy2_live = True

enemy_direction3 = "Right"
enemy_pos3X = 410
enemy_pos3Y = 107
enemy3_live = True

enemys = 3
# Game State
game_state = "Menu"

running = True
while running:
    screen.blit(bg, (0, 0))

    # End Game
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if game_state == "Playing":
        # MOVEMENTS
        new_character_X = character_posX
        new_character_Y = character_posY

        # Player Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            new_character_X -= 2
            character_direction = "Left"
            movement = True
            playerAnimation(movement, Y_collision)
        elif keys[pygame.K_d]:
            new_character_X += 2
            character_direction = "Right"
            movement = True
            playerAnimation(movement, Y_collision)
        else:
            movement = False

        # HORIZONTAL MOVEMENT
        new_character_rect = pygame.Rect(
            new_character_X, character_posY, character_width, character_heigth
        )
        X_collision = False

        playerAnimation(movement, Y_collision)

        for elements in scene:
            if elements.colliderect(new_character_rect):
                X_collision = True
                break
        if new_character_rect.left < 0 or new_character_rect.right > 800:
            X_collision = True

        if X_collision == False:
            character_posX = new_character_X

        # VERICAL MOVEMENT
        character_speed += character_aceleration
        new_character_Y += character_speed

        new_character_rect = pygame.Rect(
            character_posX, new_character_Y, character_width, character_heigth
        )
        Y_collision = False

        for elements in scene:
            if elements.colliderect(new_character_rect):
                Y_collision = True
                character_speed = 0
                if keys[pygame.K_SPACE]:
                    character_speed = -6
                    playerAnimation(movement, Y_collision)
                break

        if Y_collision == False:
            character_posY = new_character_Y

        for elements in scene:
            pygame.draw.rect(screen, "Red", elements)

        screen.blit(ground_0, (0, 380))
        screen.blit(ground_1, (400, 300))
        screen.blit(ground_2, (0, 215))
        screen.blit(ground_2, (0, 65))
        screen.blit(ground_3, (420, 140))

        # Collect Gun
        for elements in gun:
            if elements.colliderect(new_character_rect):
                gun.remove(elements)
                guns -= 1
                collect_gun.play()

        if guns == 0 and keys[pygame.K_w]:
            can_sound = not (triggered)
            if can_sound:
                shot.play()
            triggered = True

        for elements in gun:
            screen.blit(gun_image, (elements[0], elements[1]))

        # Collect ExtraLife
        for elements in extra_life:
            if elements.colliderect(new_character_rect):
                extra_life.remove(elements)
                lives += 1
                live_up.play()
            screen.blit(heart_image, (elements[0], elements[1]))

        # Shots
        if triggered == False:
            laser_posX = character_posX
            laser_posY = character_posY
            laser_direction = character_direction

        if laser_posX < -21 or laser_posX > 821:
            triggered = False

        if guns == 0 and triggered:
            if laser_direction == "Left":
                laser_posX -= 6
            else:
                laser_posX += 6
            screen.blit(laser_image, (laser_posX, laser_posY))

        new_laser_rect = pygame.Rect(laser_posX, laser_posY, 20, 8)

        for elements in scene:
            if elements.colliderect(new_laser_rect):
                triggered = False

        # Enemys
        # Enemy1
        if enemy_pos1X < 400:
            enemy_direction1 = "Right"
        elif enemy_pos1X > 750:
            enemy_direction1 = "Left"

        if enemy_direction1 == "Left" and enemy1_live:
            enemy_pos1X -= 2
            enemyAnimation()
            screen.blit(
                pygame.transform.flip(enemy_surf, True, False),
                (enemy_pos1X, enemy_pos1Y),
            )
        elif enemy_direction1 == "Right" and enemy1_live:
            enemy_pos1X += 2
            enemyAnimation()
            screen.blit(enemy_surf, (enemy_pos1X, enemy_pos1Y))

        new_enemy1_rect = pygame.Rect(
            enemy_pos1X, enemy_pos1Y, enemy_width, enemy_height
        )

        if new_enemy1_rect.colliderect(new_character_rect) and enemy1_live:
            enemy_hit.play()
            lives -= 1
            enemy_pos1X = 700
            character_posY = 340
            character_posX = 40

            if lives == 0:
                game_state = "Lose"

        if new_enemy1_rect.colliderect(new_laser_rect) and triggered and enemy1_live:
            shot_hit.play()
            enemys -= 1
            enemy1_live = False
            triggered = False

        # Enemy2
        if enemy_pos2X < 10:
            enemy_direction2 = "Right"
        elif enemy_pos2X > 315:
            enemy_direction2 = "Left"

        if enemy_direction2 == "Left" and enemy2_live:
            enemy_pos2X -= 2
            enemyAnimation()
            screen.blit(
                pygame.transform.flip(enemy_surf, True, False),
                (enemy_pos2X, enemy_pos2Y),
            )

        elif enemy_direction2 == "Right" and enemy2_live:
            enemy_pos2X += 2
            enemyAnimation()
            screen.blit(enemy_surf, (enemy_pos2X, enemy_pos2Y))

        new_enemy2_rect = pygame.Rect(
            enemy_pos2X, enemy_pos2Y, enemy_width, enemy_height
        )

        if new_enemy2_rect.colliderect(new_character_rect) and enemy2_live:
            enemy_hit.play()
            lives -= 1
            enemy_pos2X = 10
            character_posY = 340
            character_posX = 40

            if lives == 0:
                game_state = "Lose"

        if new_enemy2_rect.colliderect(new_laser_rect) and triggered and enemy2_live:
            shot_hit.play()
            enemys -= 1
            enemy2_live = False
            triggered = False

        # Enemy3
        if enemy_pos3X < 420:
            enemy_direction3 = "Right"
        elif enemy_pos3X > 750:
            enemy_direction3 = "Left"

        if enemy_direction3 == "Left" and enemy3_live:
            enemy_pos3X -= 2
            enemyAnimation()
            screen.blit(
                pygame.transform.flip(enemy_surf, True, False),
                (enemy_pos3X, enemy_pos3Y),
            )
        elif enemy_direction3 == "Right" and enemy3_live:
            enemy_pos3X += 2
            enemyAnimation()
            screen.blit(enemy_surf, (enemy_pos3X, enemy_pos3Y))

        new_enemy3_rect = pygame.Rect(
            enemy_pos3X, enemy_pos3Y, enemy_width, enemy_height
        )

        if new_enemy3_rect.colliderect(new_character_rect) and enemy3_live:
            enemy_hit.play()
            lives -= 1
            enemy_pos3X = 700
            character_posY = 340
            character_posX = 40

            if lives == 0:
                game_state = "Lose"

        if new_enemy3_rect.colliderect(new_laser_rect) and triggered and enemy3_live:
            shot_hit.play()
            enemys -= 1
            enemy3_live = False
            triggered = False

        if enemys == 0:
            game_state = "Win"

        # Player Display
        if character_direction == "Right":
            screen.blit(character_surf, (character_posX, character_posY))
        elif character_direction == "Left":
            screen.blit(
                pygame.transform.flip(character_surf, True, False),
                (character_posX, character_posY),
            )

        for l in range(lives):
            drawText("Lives: ", 0, 15, "Red", "G")

            screen.blit(heart_image, (60 + (l * 25), 5))
    elif game_state == "Menu":
        # Restarting the Game
        enemy1_live = True
        enemy2_live = True
        enemy3_live = True

        lives = 3
        enemys = 3

        character_posY = 340
        character_posX = 40

        guns = 1
        gun = [pygame.Rect(30, 45, 28, 15)]

        extra_life = [pygame.Rect(300, 25, 40, 40)]

        screen.fill("White")

        mouse_pos = pygame.mouse.get_pos()
        if play_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), play_rect)
            drawText("PLAY", 385, 65, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                game_state = "Playing"
        else:
            pygame.draw.rect(screen, "Black", play_rect)
            drawText("PLAY", 385, 65, "Red", "G")

        if inst_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), inst_rect)
            drawText("INSTRUCTIONS", 335, 155, "Red", "G")
            if event.type == pygame.MOUSEBUTTONUP:
                game_state = "Instruction"

        else:
            pygame.draw.rect(screen, "Black", inst_rect)
            drawText("INSTRUCTIONS", 335, 155, "Red", "G")

        if exit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), exit_rect)
            drawText("EXIT", 385, 240, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                running = False
        else:
            pygame.draw.rect(screen, "Black", exit_rect)
            drawText("EXIT", 385, 240, "Red", "G")

        if music_on:
            screen.blit(music1, (740, 320))
            pygame.mixer.music.set_volume(0.3)

            if music_rect.collidepoint(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    music_on = False
                    timer()

        else:
            screen.blit(music2, (740, 320))
            pygame.mixer.music.set_volume(0)

            if music_rect.collidepoint(mouse_pos):
                if event.type == pygame.MOUSEBUTTONDOWN:
                    music_on = True
                    timer()

    elif game_state == "Instruction":
        mouse_pos = pygame.mouse.get_pos()
        screen.fill("white")

        drawText("Use A to move yourself to the Left", 100, 50, "Black", "G")
        drawText("Use D to move yourself to the Right", 100, 75, "Black", "G")
        drawText("Use SPACE to jump", 100, 100, "Black", "G")
        drawText("Use W to shoot (if weapon is collected)", 100, 125, "Black", "G")

        if back_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), back_rect)
            drawText("BACK", 385, 320, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                game_state = "Menu"
        else:
            pygame.draw.rect(screen, "Black", back_rect)
            drawText("BACK", 385, 320, "Red", "G")

    elif game_state == "Lose":
        screen.fill("White")
        drawText("You Lose!", 310, 100, "Red", "end")
        mouse_pos = pygame.mouse.get_pos()

        if menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), menu_rect)
            drawText("MENU", 385, 320, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                game_state = "Menu"
        else:
            pygame.draw.rect(screen, "Black", menu_rect)
            drawText("MENU", 385, 320, "Red", "G")

        if exit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), exit_rect)
            drawText("EXIT", 385, 240, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                running = False
        else:
            pygame.draw.rect(screen, "Black", exit_rect)
            drawText("EXIT", 385, 240, "Red", "G")

    elif game_state == "Win":
        screen.fill("White")
        drawText("You Win!", 330, 100, "Green", "end")
        mouse_pos = pygame.mouse.get_pos()

        if menu_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), menu_rect)
            drawText("MENU", 385, 320, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                game_state = "Menu"
        else:
            pygame.draw.rect(screen, "Black", menu_rect)
            drawText("MENU", 385, 320, "Red", "G")

        if exit_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (33, 33, 33), exit_rect)
            drawText("EXIT", 385, 240, "Red", "G")

            if event.type == pygame.MOUSEBUTTONUP:
                running = False
        else:
            pygame.draw.rect(screen, "Black", exit_rect)
            drawText("EXIT", 385, 240, "Red", "G")

    pygame.display.update()
    clock.tick(60)


pygame.quit()
exit()