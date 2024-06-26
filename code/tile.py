from typing import Any
import pygame 
from settings import *
from Room import Room
from enemy import *
import sys

class Tile(pygame.sprite.Sprite):
	def __init__(self,pos,groups):
		super().__init__(groups)
		self.image = pygame.Surface((TILESIZE, TILESIZE))
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(0, -2)
		
class StaticTile(Tile):
	def __init__(self, pos, groups, surface):
		super().__init__(pos, groups)
		self.image = surface
          
class MessageTile(StaticTile):
	def __init__(self, pos, groups, surface, message):
		super().__init__(pos, groups, surface)
		self.message = message

class EnemySpawn(pygame.sprite.Sprite):
    def __init__(self, pos, groups, mob_spawn, room, obstacle_sprites, player, visible_sprites):
        super().__init__(groups)
        if mob_spawn < 6:
            name = 'bamboo'
        elif mob_spawn < 9:
            name = 'squid'
        else:
            name = 'spirit'
        
        self.room = room
        self.enemy = Enemy(groups, obstacle_sprites, name, pos, player, visible_sprites)
        self.rect = self.enemy.rect
        self.hitbox = self.rect.inflate(0, -6)
        self.image = self.enemy.image
    
    def fight (self, projectile):
        if projectile.hitbox.colliderect(self.hitbox) and projectile.isKilled == 0:
            self.enemy.get_damage(self.enemy.player)
            projectile.kill_count += 1
    
    def update(self):
        self.enemy.update()
        self.enemy.enemy_update(self.enemy.player)
        self.rect = self.enemy.rect
        self.hitbox = self.enemy.hitbox
        self.image = self.enemy.image
        if self.enemy.health <= 0 :
            self.enemy.player.kill_count += 1
            if self.enemy.player.kill_count % 15 == 0:
                self.enemy.player.max_health += 25
            if self.enemy.player.kill_count % 25 == 0:
                self.enemy.player.damage += 5
            if self.enemy.player.kill_count % 90 == 0:
                self.enemy.player.damage +=5
                self.enemy.player.attacking_cooldown -= 100
            self.room.enemy_count -= 1
            for group in self.groups():
                group.remove(self)

class BetterEnemiesSpawn(pygame.sprite.Sprite):
    def __init__(self, pos, groups, mob_spawn, room, obstacle_sprites, player, visible_sprites):
        super().__init__(groups)
        if mob_spawn < 4:
            name = 'bamboo'
        elif mob_spawn < 8:
            name = 'squid'
        else:
            name = 'spirit'
        
        self.room = room
        self.enemy = Enemy(groups, obstacle_sprites, name, pos, player, visible_sprites)
        self.rect = self.enemy.rect
        self.hitbox = self.rect.inflate(0, -6)
        self.image = self.enemy.image
    
    def fight (self, projectile):
        if projectile.hitbox.colliderect(self.hitbox) and projectile.isKilled == 0:
            self.enemy.get_damage(self.enemy.player)
            projectile.kill_count += 1
    
    def update(self):
        self.enemy.update()
        self.enemy.enemy_update(self.enemy.player)
        self.rect = self.enemy.rect
        self.hitbox = self.enemy.hitbox
        self.image = self.enemy.image
        if self.enemy.health <= 0 :
            self.enemy.player.kill_count += 1
            if self.enemy.player.kill_count % 15 == 0:
                self.enemy.player.max_health += 25
            if self.enemy.player.kill_count % 25 == 0:
                self.enemy.player.damage += 5
            if self.enemy.player.kill_count % 90 == 0:
                self.enemy.player.damage +=5
                self.enemy.player.attacking_cooldown -= 100
            self.room.enemy_count -= 1
            for group in self.groups():
                group.remove(self)


class BossSpawn(pygame.sprite.Sprite):
    def __init__(self, pos, groups, mob_spawn, room, obstacle_sprites, player, visible_sprites):
        super().__init__(groups)
        
        self.room = room
        self.enemy = Enemy(groups, obstacle_sprites, 'raccoon', pos, player, visible_sprites)
        self.rect = self.enemy.rect
        self.hitbox = self.rect.inflate(0, -6)
        self.image = self.enemy.image
    
    def fight (self, projectile):
        if projectile.hitbox.colliderect(self.hitbox) and projectile.isKilled == 0:
            self.enemy.get_damage(self.enemy.player)
            projectile.kill_count += 1
    
    def update(self):
        self.enemy.update()
        self.enemy.enemy_update(self.enemy.player)
        self.rect = self.enemy.rect
        self.hitbox = self.enemy.hitbox
        self.image = self.enemy.image
        if self.enemy.health <= 0 :
            self.enemy.player.kill_count += 1
            if self.enemy.player.kill_count % 15 == 0:
                self.enemy.player.max_health += 999
            if self.enemy.player.kill_count % 25 == 0:
                self.enemy.player.damage += 999
            self.room.enemy_count -= 1
            for group in self.groups():
                group.remove(self)
            self.handle_death()

    def handle_death(self):
        victory = pygame.image.load('../Victory.png')
        victory = pygame.transform.scale(victory, (WIDTH, HEIGTH))
        screen = pygame.display.get_surface()
        screen.blit(victory, (0, 0))
        victory_sound = pygame.mixer.Sound('../audio/main.ogg')
        victory_sound.set_volume(config.volume)
        victory_sound.play()
        pygame.display.flip()
        end_time = pygame.time.get_ticks() + 126000
        while pygame.time.get_ticks() < end_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.flip()