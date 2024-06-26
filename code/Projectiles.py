import pygame
from support import *
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, start_pos, damage, player, obstacle_sprites):
        super().__init__()
        self.obstacle_sprites = obstacle_sprites
        self.player = player

        self.damage = damage
        self.speed = 2
        self.direction = pygame.math.Vector2()

        self.frame_index = 0
        self.animation_speed = 0.15
        self.last_update = pygame.time.get_ticks()

        original_image = import_folder("../assets/fireball")

        self.isKilled = 0
        self.zoom_factor = 0.25

        self.image = pygame.transform.scale(original_image[self.frame_index], (64, 32))
        self.rect = self.image.get_rect(topleft=start_pos)
        scaled_width = int(self.rect.width * self.zoom_factor)
        scaled_height = int(self.rect.height * self.zoom_factor)
        self.rect = pygame.Rect(self.rect.x, self.rect.y, scaled_width, scaled_height)
        self.hitbox = self.rect

        self.images = original_image
        self.image = self.images[self.frame_index]
        self.rect = self.image.get_rect(topleft=start_pos)
        scaled_width = int(self.rect.width * self.zoom_factor)
        scaled_height = int(self.rect.height * self.zoom_factor)
        self.rect = pygame.Rect(self.rect.x, self.rect.y, scaled_width, scaled_height)
        self.hitbox = self.rect


    def set_direction(self, direction):
        self.direction = direction
        
    def update(self):
        self.rect.move_ip(self.direction * self.speed)
        for obstacle in self.obstacle_sprites:
            if pygame.sprite.collide_rect(self, obstacle):
                self.kill()
                self.isKilled = 1
                break 
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed * 1000:
            self.last_update = now
            self.frame_index = (self.frame_index + 1) % len(self.images) 

            angle = math.atan2(-self.direction.y, self.direction.x) * 180 / math.pi
            self.image = pygame.transform.rotate(self.images[self.frame_index], angle)
            self.rect = self.image.get_rect(center=self.rect.center)
            self.rect = self.rect.inflate(16 - self.rect.width, 8 - self.rect.height)
            self.hitbox = self.rect

        if pygame.sprite.collide_rect(self, self.player):
            if (self.player.vulnerable == True):
                self.player.health -= self.damage
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
            self.isKilled = 1
            self.kill()
