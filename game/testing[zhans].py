import pygame
import time
from spriteclasses import Player, Door, Wall
from interaction import Interactable
from lighting import Dim, Light
from soundbar import sfx
from menu_testing import*

pygame.init()
screen = pygame.display.set_mode((1280, 720))

bg_room1 = pygame.transform.scale(pygame.image.load('images/room/room1.png'), (1280, 720))
bg_room2 = pygame.transform.scale(pygame.image.load('images/room/room2.png'), (1280, 720))
bg_room3 = pygame.transform.scale(pygame.image.load('images/room/room3.png'), (1280, 720))
bg_room4 = pygame.transform.scale(pygame.image.load('images/room/room4.png'), (1280, 720))
bg_room5 = pygame.transform.scale(pygame.image.load('images/room/room5.png'), (1280, 720))

clock = pygame.time.Clock()

player = Player(screen, (50, 600))

wall1 = Wall((0, 0), (1280, 200))
table_border = Wall((240, 280), (250, 80))
door = Door(screen, (600, 60))

notebook = Interactable(1, (195, 280, 250, 120), (255, 255, 255), room="room1", item="notebook")
puddle = Interactable(1, (950, 280, 200, 200), (255, 255, 255), room="room1", item="puddle")

lantern = Light(screen, (220, 220, 220), 25, (player.rect.x + 97, player.rect.y + 152))
dim = Dim(screen)


bgm_channel = pygame.mixer.Channel(0)
sfx_channel = pygame.mixer.Channel(1)

current_room = "room1"
current_room_bg = bg_room1
game_menu(bgm_channel, sfx_channel, "main")
def scene1():
    global current_room, current_room_bg
    door_open_time = 0
    run = True
    while run:
        screen.blit(current_room_bg, (0, 0))
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z and (player.rect.x > 600) and (player.rect.y < 210):
                    if notebook.rect.colliderect(player.rect):
                        notebook.enable = True
                    if puddle.rect.colliderect(player.rect):
                        puddle.enable = True
                    if door.rect.colliderect(player.rect) and time.time() - door_open_time > 2:
                        door.open_door()
                        door_open_time = time.time()
                        if current_room == "room1":
                            current_room = "room2"
                            current_room_bg = bg_room2
                            player.rect.x = 50
                            player.rect.y = 380
                            door.close_door()
                        elif current_room == "room2":
                            current_room = "room3"
                            current_room_bg = bg_room3
                            player.rect.x = 50
                            player.rect.y = 380
                            door.close_door()
                        elif current_room == "room3":
                            current_room = "room4"
                            current_room_bg = bg_room4
                            player.rect.x = 50
                            player.rect.y = 380
                            door.close_door()
                        elif current_room == "room4":
                            current_room = "room5"
                            current_room_bg = bg_room5
                            player.rect.x = 50
                            player.rect.y = 380
                            door.close_door()
                if event.key == pygame.K_ESCAPE:
                    game_menu(bgm_channel, sfx_channel, "pause")
                    pygame.mixer.pause()

        keys = pygame.key.get_pressed()

        player.move(keys, lantern)

        door.blit()
        player.blit()

        dim.darken(150)

        lantern.blit((100, 100, 100), size=5)

        notebook.interaction(player, screen, keys)
        puddle.interaction(player, screen, keys)

        player.wall_collision(Wall.walls)

        pygame.display.update()

scene1()
