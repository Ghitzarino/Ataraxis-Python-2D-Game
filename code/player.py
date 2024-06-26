import pygame
from settings import *
from debug import debug
from math import sin
from support import import_folder
from tile import EnemySpawn, BetterEnemiesSpawn, BossSpawn
import sys
import config

game_over_sound = pygame.mixer.Sound('../audio/game_over.wav')
game_over_sound.set_volume(config.volume)

class Player(pygame.sprite.Sprite):
	def __init__(self, pos, groups, obstacle_sprites, create_attack, destroy_sword_attack, type_character):
		super().__init__(groups)
		self.zoom_factor = 0.25

		self.kill_count = 0
		self.choice = type_character

		self.vulnerable = True
		self.hurt_time = pygame.time.get_ticks()
		self.invincibility_duration = 800
		self.current_attack = []

		original_image = pygame.image.load('../graphics/player/down_idle/down_idle.png').convert_alpha()
		self.image = pygame.transform.scale(original_image, (64, 64))
		self.rect = self.image.get_rect(topleft=pos)
		scaled_width = int(self.rect.width * self.zoom_factor)
		scaled_height = int(self.rect.height * self.zoom_factor)
		self.rect = pygame.Rect(self.rect.x, self.rect.y, scaled_width, scaled_height)
		self.hitbox = self.rect.inflate(0, -6)
		
		self.obstacle_sprites = obstacle_sprites
		self.direction = pygame.math.Vector2()

		self.attacking = False
		self.ability = False
		self.attacking_cooldown = 1000
		self.attack_time = None
		self.ability_time = None
		self.create_attack = create_attack
		self.destroy_sword_attack = destroy_sword_attack

		if self.choice == 'Knight':
			self.weapon_attack_sound = pygame.mixer.Sound('../audio/sword.wav')
			self.weapon_attack_sound.set_volume(config.volume)
		elif self.choice == 'Archer':
			self.weapon_attack_sound = pygame.mixer.Sound('../audio/attack/bow.mp3')
			self.weapon_attack_sound.set_volume(config.volume)
		elif self.choice == 'Mage':
			self.weapon_attack_sound = pygame.mixer.Sound('../audio/attack/fireball.wav')
			self.weapon_attack_sound.set_volume(config.volume)

		self.ability_sound = pygame.mixer.Sound('../audio/heal.wav')
		self.ability_sound.set_volume(config.volume)

		self.weapon = 'sword'

		self.max_health = 0
		self.health = 100
		self.mana = 50
		self.damage = 10
		self.speed = 100
		self.get_class_stats()

		self.import_player_assets()
		self.status = 'down'
		self.frame_index = 0
		self.animation_speed = 0.15

	def get_class_stats(self):
		if self.choice == 'Knight':
			self.weapon = 'sword'
			stats = {'health': 150, 'mana': 30, 'attack': 15, 'magic': 5, 'speed': 3, 'attacking_cooldown': 500}
		elif self.choice == 'Mage':
			self.weapon = 'wand'
			stats = {'health': 100, 'mana': 50, 'attack': 18, 'magic': 20, 'speed': 2, 'attacking_cooldown': 700}
		elif self.choice == 'Archer':
			self.weapon = 'bow'
			stats = {'health': 120, 'mana': 40, 'attack': 12, 'magic': 8, 'speed': 3, 'attacking_cooldown': 450}

		self.max_health = stats['health']
		self.health = stats['health']
		self.mana = stats['mana']
		self.speed = stats['speed']
		self.damage = stats['attack']
		self.magic = stats['magic'] 
		self.attacking_cooldown = stats['attacking_cooldown']

	def get_status(self):

		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status += '_idle'
		
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle', '_attack')
				else:
					self.status += '_attack'
		elif 'attack' in self.status:
			self.status = self.status.replace('_attack', '')

	def import_player_assets(self):
		player_path = "../graphics/player/"
		self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
			'up_idle': [], 'down_idle': [], 'left_idle': [], 'right_idle': [],
			'up_attack': [], 'down_attack': [], 'left_attack': [], 'right_attack': []}
		
		for animation in self.animations.keys():
			full_path = player_path + animation
			if 'attack' in animation:
				full_path += '/' + self.weapon

			self.animations[animation] = import_folder(full_path)

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()

			if keys[pygame.K_w]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_s]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0

			if keys[pygame.K_a]:
				self.direction.x = -1
				self.status = 'left'
			elif keys[pygame.K_d]:
				self.direction.x = 1
				self.status = 'right'
			else:
				self.direction.x = 0

			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()
				self.weapon_attack_sound.play()
			
			if keys[pygame.K_LSHIFT] and self.ability == False:
				self.ability = True
				self.ability_time = pygame.time.get_ticks()
				self.magic_ability()
				self.ability_sound.play()

	def magic_ability(self):
		if (self.choice == 'Knight'):
			self.health += 50
			self.damage += 5
		elif self.choice == 'Archer':
			self.speed += 1
			self.attacking_cooldown -= 150

		elif self.choice == 'Mage':
			self.damage += 7
			self.attacking_cooldown -= 100

	def reverse_magic(self):
		if (self.choice == 'Knight'):
			if (self.health > self.max_health):
				self.health = self.max_health
			self.damage -= 5
		elif self.choice == 'Archer':
			self.speed -= 1
			self.attacking_cooldown += 150

		elif self.choice == 'Mage':
			self.damage -= 7
			self.attacking_cooldown += 100

	def move(self, speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()

		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center
	
	def collision(self, direction):

		if direction == 'horizontal':
			for obstacle in self.obstacle_sprites:
				if obstacle.hitbox.colliderect(self.hitbox):
					if self.direction.x > 0:
						self.hitbox.right = obstacle.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = obstacle.hitbox.right

		if direction == 'vertical':
			for obstacle in self.obstacle_sprites:
				if obstacle.hitbox.colliderect(self.hitbox):
					if self.direction.y > 0:
						self.hitbox.bottom = obstacle.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = obstacle.hitbox.bottom
						
		for group in self.groups():
			for sprite in group:
				if isinstance(sprite, EnemySpawn) or isinstance(sprite, BetterEnemiesSpawn) or isinstance(sprite, BossSpawn):
					for projectile in self.current_attack:
						sprite.fight(projectile)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attacking_cooldown:
				self.attacking = False

			if self.choice == 'Knight' and current_time - self.attack_time >= 100:
				self.destroy_sword_attack()

		if self.ability:
			if current_time - self.ability_time >= 5000:
				self.ability = False
				self.reverse_magic()

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invincibility_duration:
				self.vulnerable = True

	def animate(self):
		animation = self.animations[self.status]

		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0

		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)

		if not self.vulnerable:
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def wave_value(self):
		value = sin(pygame.time.get_ticks())
		if value >= 0: 
			return 255
		else: 
			return 0

	def update(self):
		self.input()
		self.move(self.speed)
		self.cooldowns()
		self.get_status()
		self.animate()

		if self.health <= 0:
			self.handle_death()
			
	def handle_death(self):
		game_over_screen = pygame.image.load('../GameOver.png')
		game_over_screen = pygame.transform.scale(game_over_screen, (WIDTH, HEIGTH))
		screen = pygame.display.get_surface()
		screen.blit(game_over_screen, (0, 0))
		game_over_sound.play()
		pygame.display.flip()
		pygame.time.delay(3000)
		pygame.quit()
		sys.exit()