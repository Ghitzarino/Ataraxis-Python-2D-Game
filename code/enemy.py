import pygame
from entity import Entity
from support import *
from Projectiles import Projectile

import pygame.surfarray as surfarray
import numpy as np
import config

class Enemy(Entity):

    def __init__(self, groups, obstacle_sprites, monster_name,pos, player, visible_sprites):

        super().__init__(groups, obstacle_sprites, visible_sprites)
        self.sprite_type = 'enemy'

        self.projectiles = []
        self.player = player


        self.frame_index = 0
        self.animation_speed = 0.15
        self.import_graphics(monster_name)
        self.status = 'idle'

        self.zoom_factor = 0.25

        self.image = self.animations[self.status][self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-2)
        self.health = 0
        self.speed = 0
        self.attack_damage = 0
        self.resistance = 0
        self.attack_radius = 0
        self.notice_radius = 0
        self.attack_type = ''
        self.max_health = self.health

        self.death_sound = pygame.mixer.Sound('../audio/death.wav')
        self.hit_sound = pygame.mixer.Sound('../audio/hit.wav')
        self.growl = pygame.mixer.Sound('../audio/growl.mp3')
        self.death_sound.set_volume(config.volume)
        self.hit_sound.set_volume(config.volume)
        self.growl.set_volume(config.volume)

        self.monster_name = monster_name
        if monster_name == 'raccoon':
            self.health = 400
            self.max_health = self.health
            self.speed = 1
            self.attack_damage = 20
            self.resistance = 1
            self.attack_radius = 30
            self.notice_radius = 300
            self.attack_type = 'slash'
        if monster_name == 'bamboo':
            self.health = 35
            self.speed = 1
            self.attack_damage = 10
            self.resistance = 1
            self.attack_radius = 20
            self.notice_radius = 150
            self.attack_type = 'slash'
        if monster_name == 'spirit':
            self.health = 15
            self.speed = 1
            self.attack_damage = 20
            self.resistance = 2
            self.attack_radius = 5
            self.notice_radius = 150
            self.attack_type = 'kamikaze'
        if monster_name == 'squid':
            self.health = 15
            self.speed = 1
            self.attack_damage = 10
            self.resistance = 1
            self.attack_radius = 80
            self.notice_radius = 150
            self.attack_type = 'circle_attack'

        self.can_attack = True
        self.attack_time = pygame.time.get_ticks()
        self.attack_cooldown = 1500
        self.last_attack_time = 0

        self.vulnerable = True
        self.hit_time = None
        self.invincibility_duration = 300
        self.isPhase2 = False

    def import_graphics(self,name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'../assets/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.notice_radius:
            self.status = 'move'
            if (self.monster_name == 'squid' and distance <= self.attack_radius):
                self.status = 'idle'
        else:
            self.status = 'idle'
    
    def circle_attack(self, player):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_attack_time < self.attack_cooldown:
            return

        projectile = Projectile((self.rect.left, self.rect.centery), self.attack_damage, self.player, self.obstacle_sprites)
        direction = self.get_player_distance_direction(self.player)[1]
        
        projectile.set_direction(direction)
        self.projectiles.append(projectile)
        self.visible_sprites.add(projectile)
        self.last_attack_time = current_time
    
    def intensify_red(self, image):
        image = image.convert_alpha()

        rgb_array = pygame.surfarray.array3d(image)
        alpha_array = pygame.surfarray.array_alpha(image)

        rgba_array = np.dstack((rgb_array, alpha_array))

        alpha_threshold = 10

        mask = (rgba_array[:,:,-1] > alpha_threshold) & (rgba_array[:,:,0] > 0)

        rgba_array[mask, 0] = np.minimum(rgba_array[mask, 0] * 1.5, 255).astype(np.uint8)

        rgba_array[mask, 1:3] = (rgba_array[mask, 1:3] * 0.75).astype(np.uint8)

        rgb_array = rgba_array[:,:,:3]
        alpha_array = rgba_array[:,:,-1]

        new_image = pygame.Surface(image.get_size(), pygame.SRCALPHA)
        pygame.surfarray.blit_array(new_image, rgb_array)
        pygame.surfarray.pixels_alpha(new_image)[:] = alpha_array

        return new_image

    
    def actions(self,player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            if self.attack_type == 'circle_attack':
                self.circle_attack(player)
            elif self.attack_type == 'kamikaze':
                self.direction = self.get_player_distance_direction(player)[1]
                if self.get_player_distance_direction(player)[0] <= 20:
                    self.health = -1
                    self.damage_player(player)
            elif self.monster_name == 'raccoon' and self.health < 0.5 * self.max_health:
                if self.isPhase2 == False:
                    self.growl.play()
                    self.isPhase2 = True
                    self.attack_damage += 10
                    self.attack_cooldown -= 300
                self.damage_player(player)
            else:
                self.damage_player(player)
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False

            self.frame_index = 0

        if self.monster_name == 'raccoon' and self.health < 0.5 * self.max_health:
            self.image = self.intensify_red(animation[int(self.frame_index)])
        else:
            self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def damage_player(self,player):
        if player.vulnerable:
            player.health -= self.attack_damage
            player.vulnerable = False
            player.hurt_time = pygame.time.get_ticks()
            player.direction = self.get_player_distance_direction(self.player)[1]

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self,player):
        if self.vulnerable:
            self.hit_sound.play()
            self.direction = self.get_player_distance_direction(player)[1]
            self.health -= player.damage
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False
    
    def hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):    
        self.hit_reaction()
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        for projectile in self.projectiles:
            if projectile.isKilled == 0:
                projectile.update()