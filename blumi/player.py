import pygame
import random

class Player(pygame.sprite.Sprite):

    def __init__(self, gameover, x, y):
        pygame.sprite.Sprite.__init__(self)
        
        self.last_update = pygame.time.get_ticks()
        self.anim_rate = 100
        self.flap_flag = False
        self.frame = 0
        self.get_flap()

        if self.flap_flag == True:
            self.image = self.flap_anim[self.frame]
        else:    
            self.image = pygame.image.load("BlumiBird/assets/sprite_0.png")

        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vel = 0
        self.counter = 0
        self.gameover = gameover
        
    
    def update(self):
        """Main Birb Function, controlls the bird and sets its animation"""

        #Gravity (y-Acceleration)
        if self.rect.center[1] > 1150:
            self.vel = 0
            self.gameover = True

        else:
            if self.vel >= 18:
                self.vel = 18
            else:
                self.vel += 0.8

        self.counter += 1

        # desperate try for an animation
        now = pygame.time.get_ticks()
        if self.flap_flag == True:
            if now - self.last_update > self.anim_rate:
                self.last_update = now
                self.frame += 1
                if self.frame >= len(self.flap_anim):
                    self.flap_flag = False
                    self.frame = 0
                self.center = self.rect.center
                self.image = self.flap_anim[self.frame]
                self.rect.center = self.center

        else:    
            self.image = pygame.image.load("BlumiBird/assets/sprite_0.png")
        # print(self.flap_flag)

        #Jumping
        events = pygame.event.get()
        for event in events:
            if self.gameover != True:
                if event.type == pygame.KEYDOWN and self.counter > 20:
                    # print("keydown")
                    self.flap_flag = True
                    if self.rect.center[1] > 50:
                        self.vel = -15


        # print(self.vel)
        
        self.rect.y += int(self.vel)
    
    def get_flap(self):
        """Sets up the Flying Animation Frames"""
        print("setting anim")
        sprite_0 = pygame.image.load("BlumiBird/assets/sprite_0.png")
        sprite_1 = pygame.image.load("BlumiBird/assets/sprite_1.png")
        sprite_2 = pygame.image.load("BlumiBird/assets/sprite_2.png")
        self.flap_anim = [sprite_0,
                          sprite_1,
                          sprite_2]


class Pipes(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('BlumiBird/assets/Chimney.png')
        # self.image = pygame.transform.scale(self.image,)
        self.rect = self.image.get_rect()
        if position == -1:
            self.image = pygame.transform.flip(self.image, True, False)
            self.rect.bottomleft = [x, y]
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.topleft = [x, y]

    def update(self):
        self.rect.x -= 4