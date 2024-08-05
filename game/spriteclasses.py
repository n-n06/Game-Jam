
import pygame
import os
from soundbar import sfx
pygame.init()

from config import screen
from utils import scene_literal

class Player(pygame.sprite.Sprite):

    def __init__(self, pos):

        super().__init__()
        self.screen = screen


        self.walk_left_images = [
            pygame.image.load('images/sprites/Boy/left/' + x) for x in os.listdir('images/sprites/Boy/left')
        ]

        self.walk_right_images = [
            pygame.image.load('images/sprites/Boy/right/' + x) for x in os.listdir('images/sprites/Boy/right')
        ]

        self.walk_face_images = [
            pygame.image.load('images/sprites/Boy/face/' + x) for x in os.listdir('images/sprites/Boy/face')
        ]

        self.walk_back_images = [
            pygame.image.load('images/sprites/Boy/back/' +x) for x in os.listdir('images/sprites/Boy/back')
        ]

        self.default_image = self.walk_face_images[0]
        self.rect = self.default_image.get_rect(center = pos)
        self.old_x = 0
        self.old_y = 0

        self.speed = 8

        self.moving = {
                "left" : False,
                "right" : False,
                "face" : False,
                "back" : False
        }

        self.walk_count = 0
        #self.up
        #self.down


    def move(self, pressed, lantern):
        self.old_x = self.rect.x
        self.old_y = self.rect.y

        if pressed[pygame.K_UP]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["back"] = True
            self.rect.y = max(self.rect.y - self.speed, 0)
            lantern.pos = (self.rect.x+97, self.rect.y+152)

        elif pressed[pygame.K_DOWN]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["face"] = True
            self.rect.y = min(self.rect.y + self.speed, self.screen.get_height()-self.rect.height)
            lantern.pos = (self.rect.x + 97, self.rect.y + 152)

        elif pressed[pygame.K_LEFT]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["left"] = True
            self.rect.x = max(0, self.rect.x - self.speed)
            lantern.pos = (self.rect.x + 15, self.rect.y + 182)

        elif pressed[pygame.K_RIGHT]:
            for key in self.moving.keys():
                self.moving[key] = False
            self.moving["right"] = True
            self.rect.x = min(self.screen.get_width() - self.rect.width, self.rect.x + self.speed)
            lantern.pos = (self.rect.x + self.rect.width + 30, self.rect.y + 182)
        else:
            self.moving["right"] = False
            self.moving["left"] = False
            self.walk_count = 0
            lantern.pos = (self.rect.x + 97, self.rect.y + 152)


    def blit(self):
        if self.walk_count + 1 >= 60:
            self.walk_count = 0

        if self.moving["left"]:
            self.screen.blit(self.walk_left_images[self.walk_count // 12], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.moving["right"]:
            self.screen.blit(self.walk_right_images[self.walk_count // 12], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.moving["face"]:
            self.screen.blit(self.walk_face_images[self.walk_count // 20], (self.rect.x, self.rect.y))
            self.walk_count += 1
        elif self.moving["back"]:
            self.screen.blit(self.walk_back_images[self.walk_count // 20], (self.rect.x, self.rect.y))
            self.walk_count += 1
        else:
            self.screen.blit(self.default_image, (self.rect.x, self.rect.y))

    def wall_collision(self, walls):
        self.rect.x += (self.rect.x-self.old_x)
        wall_hit_list = (wall for wall in walls if pygame.sprite.collide_rect(self, wall))
        for wall in wall_hit_list:
            if (self.rect.x - self.old_x) > 0:
                self.rect.right = wall.rect.left
            elif (self.rect.x - self.old_x) < 0:
                self.rect.left = wall.rect.right

        self.rect.y += (self.rect.y - self.old_y)
        wall_hit_list = (wall for wall in walls if pygame.sprite.collide_rect(self, wall))

        for wall in wall_hit_list:
            if (self.rect.y - self.old_y) > 0:
                self.rect.bottom = wall.rect.top
            elif (self.rect.y - self.old_y) < 0:
                self.rect.top = wall.rect.bottom


class Witch(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.screen = screen
        self.scare_trigger = False
        self.image =pygame.image.load("images/sprites/monster/monster_big.png")
        self.scream_image = pygame.transform.scale(pygame.image.load("images/sprites/monster/scream.png"), (1280,720))
        self.rect = self.image.get_rect()
        self.sfx = sfx["jumpscare"]

        self.channel = pygame.mixer.Channel(1)

        self.ghost_image = pygame.image.load("images/sprites/monster/ghost.png")
        self.ghost_rect = self.ghost_image.get_rect()
        self.ghost_done = False
        self.ghost_alpha = 255

    def mirage(self, pos, player):
        '''
        Blitting an image of a ghost, then gradually decreasing its alpha value to make it transparent
        '''
        self.ghost_rect.topleft = pos
        if not self.ghost_done:
            self.ghost_alpha = 255 - player.rect.left
        if self.ghost_alpha < 0:
            self.ghost_alpha = 0
            self.ghost_done = True
        self.ghost_image.set_alpha(self.ghost_alpha)
        self.screen.blit(self.ghost_image, self.ghost_rect)
        

    def scare(self, player):
        #placing the jumpsace slightly to the left of the player
        screen_center_x = self.screen.get_width() // 2
        screen_center_y = self.screen.get_height() // 2
        self.rect.center = (screen_center_x, screen_center_y)
        self.screen.blit(self.image, self.rect)
        self.channel.play(self.sfx) #playing the sound effect of the screamer
        pygame.display.flip()
        pygame.time.delay(1000) #delaying the screen for 1 second
        self.screen.blit(self.scream_image, (0,0)) #blitting the close-up of the screamer
        pygame.display.flip()
        pygame.time.delay((2000))   #delaying the screen for 2 second
        self.scare_trigger = False



class Door():
    def __init__(self, pos):
        self.screen = screen

        self.closed_image = pygame.image.load("images/door/door (1).png")
        self.open_image = pygame.image.load("images/door/door (2).png")
        self.opened = False
        self.current_image = self.closed_image

        self.pos = pos
        self.rect = self.current_image.get_rect(topleft=pos)

        self.audio_channel = pygame.mixer.Channel(2)

    def blit(self):
        self.screen.blit(self.current_image, self.rect)

    def open_door(self):
        if not self.opened:
            self.audio_channel.play(sfx["dooropen"])
            self.current_image = self.open_image
            self.opened = True

    def close_door(self):
        if self.opened:
            self.audio_channel.play(sfx["doorclose"])
            self.current_image = self.closed_image
            self.opened = False



class Wall(pygame.sprite.Sprite):
    #walls = pygame.sprite.Group()

    walls = {
        "scene1" : [],
        "scene2" : [],
        "scene3" : [],
        "scene4" : [],
        "scene5" : [],
        "scene6" : [],
        "scene7" : [],
    }
    def __init__(self, topleft : tuple[int, int], size : tuple[int, int], scene : scene_literal):
        super().__init__()
        self.x = topleft[0]
        self.y = topleft[1]
        self.width = size[0]
        self.height = size[1]
        self.show = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        Wall.walls[scene].append(self)

    def show_test(self, room):
        pass
        #for wall in Wall.walls[room]:
            #pygame.draw.rect(screen, (255,255,255), wall.rect, 4)

    @classmethod
    def delete_all(cls, scene : scene_literal):
        cls.walls[scene] = []

