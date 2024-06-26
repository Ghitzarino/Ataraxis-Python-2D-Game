import pygame
from settings import *
from tile import *
from player import Player
from debug import debug
from support import import_csv_layout, import_cut_graphics
import random
from Room import Room
from Projectiles import *
from Projectile_player import *
from ui import UI

class Level:	
	def __init__(self, level_data, type_character):

		self.display_surface = pygame.display.get_surface()

		self.ui = UI(type_character)

		self.visible_sprites = YSortCameraGroup()
		self.obstacle_sprites = pygame.sprite.Group()

		self.terrain_layout = import_csv_layout(level_data['terrain'])
		self.wall_layout = import_csv_layout(level_data['wall'])
		self.details_layout = import_csv_layout(level_data['details'])
		self.normalEnemies_layout = import_csv_layout(level_data['normalEnemies'])
		self.betterEnemies_layout = import_csv_layout(level_data['betterEnemies'])
		self.boss_layout = import_csv_layout(level_data['Boss'])

		self.message_tiles = []

		self.terrain_sprites = self.create_tile_group(self.terrain_layout, 'terrain')
		self.wall_sprites = self.create_tile_group(self.wall_layout, 'wall')
		self.details_sprites = self.create_tile_group(self.details_layout, 'details')

		self.rooms = []
		
		self.player = Player((level_data['start_x'] * TILESIZE, level_data['start_y'] * TILESIZE),[self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_sword_attack, type_character)

		for i in range(1, 21):
			string = 'room' + str(i) + 'info'
			room = Room(level_data[string], str(i))
			room.sprite_group = self.create_room_tile_group(room)
			self.rooms.append(room)

		room = Room(level_data['roomBossinfo'], 'Boss')
		room.sprite_group = self.create_room_tile_group(room)
		self.rooms.append(room)


	def create_tile_group(self, layout, type):

		message_mapping = {
				(26, 14): "Press WASD to Move",
				(26, 24): "Press LSHIFT for special ability",
				(28, 17): "Press SPACE to attack",
			}

		sprite_group = pygame.sprite.Group()
		self.type = type
		for row_index, row in enumerate(layout):
			for col_ind, val in enumerate(row):
				if val != '-1':
					x = col_ind * TILESIZE
					y = row_index * TILESIZE

					if (type == 'terrain'):
						terrain_tile_list = import_cut_graphics('../graphics/2D Pixel Dungeon Asset Pack/character and tileset/Dungeon_Tileset.png', zoom_factor = 4.0)
						tile_surface = terrain_tile_list[int(val)]
						sprite = StaticTile((x, y), [self.visible_sprites], tile_surface)
					elif type == 'wall':
						wall_tile_list = import_cut_graphics('../graphics/2D Pixel Dungeon Asset Pack/character and tileset/Dungeon_Tileset.png', zoom_factor=4.0)
						wall_surface = wall_tile_list[int(val)]
						sprite = StaticTile((x, y), [self.visible_sprites, self.obstacle_sprites], wall_surface)
					elif type == 'details':
						details_tile_list = import_cut_graphics('../graphics/2D Pixel Dungeon Asset Pack/character and tileset/Dungeon_Tileset.png', zoom_factor=4.0)
						details_surface = details_tile_list[int(val) & (2 ** 9 - 1)]
						details_surface = pygame.transform.flip(details_surface, int(val) & (2 ** 31) == (2 ** 31), int(val) & (2 ** 30) == (2 ** 30))
						if (layout[row_index][col_ind] == '75'):
							sprite = MessageTile((x, y), [self.visible_sprites], details_surface, message_mapping.get((row_index, col_ind), "SAFEZONE"))
							self.message_tiles.append(sprite)
						else:
							sprite = StaticTile((x, y), [self.visible_sprites], details_surface)
					elif type == 'normalEnemies':
						sprite = EnemySpawn((x, y), [self.visible_sprites], random.randint(1, 10))
					elif type == 'betterEnemies':
						sprite = BetterEnemiesSpawn((x, y), [self.visible_sprites], random.randint(1, 10))
					elif type == 'Boss':
						sprite = BossSpawn((x, y), [self.visible_sprites], 1)				

					sprite_group.add(sprite)

		return sprite_group

	def create_room_tile_group(self, room):
		sprite_group = pygame.sprite.Group()
		self.type = type
		for row_index, row in enumerate(room.room_sprites_layout):
			for col_ind, val in enumerate(row):
				if val != '-1':
					x = col_ind * TILESIZE
					y = row_index * TILESIZE
					if val == self.normalEnemies_layout[row_index][col_ind]:
						sprite = EnemySpawn((x, y), [], random.randint(1, 10), room, self.obstacle_sprites, self.player, self.visible_sprites)
						room.enemy_count += 1
					elif val == self.betterEnemies_layout[row_index][col_ind]:
						sprite = BetterEnemiesSpawn((x, y), [], random.randint(1, 10), room, self.obstacle_sprites, self.player, self.visible_sprites)	
						room.enemy_count += 1
					elif val == self.boss_layout[row_index][col_ind]:
						sprite = BossSpawn((x, y), [], 1, room, self.obstacle_sprites, self.player, self.visible_sprites)	
						room.enemy_count += 1
					else:
						details_tile_list = import_cut_graphics('../graphics/2D Pixel Dungeon Asset Pack/character and tileset/Dungeon_Tileset.png', zoom_factor=4.0)
						details_surface = details_tile_list[int(val) & (2 ** 9 - 1)]
						details_surface = pygame.transform.flip(details_surface, int(val) & (2 ** 31) == (2 ** 31), int(val) & (2 ** 30) == (2 ** 30))
						sprite = StaticTile((x, y), [], details_surface)
						room.obstacle_group.add(sprite)
					sprite_group.add(sprite)
		return sprite_group

	def display_message(self, message):
		font = pygame.font.Font(None, 36)
		text_surface = font.render(message, True, (255, 255, 255))
		text_rect = text_surface.get_rect(center=(self.display_surface.get_width() // 2, self.display_surface.get_height() - 50))
		self.display_surface.blit(text_surface, text_rect)

	def check_message_tiles(self, player):
		for message_tile in self.message_tiles:
			distance = pygame.math.Vector2(player.rect.center).distance_to(message_tile.rect.center)
			if distance <= TILESIZE:
				self.display_message(message_tile.message)
				break


	def run(self):
		self.visible_sprites.custom_draw(self.player)
		self.visible_sprites.update()
		n = len(self.rooms)
		for i in range(n):
			if self.rooms[i].isIn(self.player.rect.centerx, self.player.rect.centery) > 0 and self.rooms[i].playerIn == 0 and self.rooms[i].enemy_count > 0:
				self.rooms[i].playerIn = 1
				self.visible_sprites.add(self.rooms[i].sprite_group)
				self.obstacle_sprites.add(self.rooms[i].obstacle_group)
			elif self.rooms[i].playerIn == 1 and self.rooms[i].enemy_count <= 0:
				self.visible_sprites.remove(self.rooms[i].sprite_group)
				self.obstacle_sprites.remove(self.rooms[i].obstacle_group)
				if (self.player.health < self.player.max_health):
					self.player.health = self.player.max_health
				self.rooms[i].playerIn = 0
		self.check_message_tiles(self.player)
		self.destroy_projectile_attack()
		self.ui.display(self.player, self.player.ability)

	def create_attack(self):
		new_projectile = Projectile_player(self.player, [self.visible_sprites])
		self.player.current_attack.append(new_projectile)

	def destroy_sword_attack(self):
		for projectile in self.player.current_attack:
			projectile.kill()
			self.player.current_attack.remove(projectile)

	def destroy_projectile_attack(self):
		if self.player.current_attack and self.player.choice != 'Knight':
			for projectile in self.player.current_attack:
				for obstacle in self.obstacle_sprites:
					if obstacle.hitbox.colliderect(projectile.hitbox):
						projectile.kill()
						self.player.current_attack.remove(projectile)
						break 

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.zoom_factor = 4.0
		self.half_width = self.display_surface.get_size()[0] // 2
		self.half_height = self.display_surface.get_size()[1] // 2
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - self.half_width / self.zoom_factor
		self.offset.y = player.rect.centery - self.half_height / self.zoom_factor

		for sprite in self.sprites():
			if isinstance(sprite, Player) or isinstance(sprite, EnemySpawn) or isinstance(sprite, BetterEnemiesSpawn) or isinstance(sprite, BossSpawn):
				aux = sprite.image
				if isinstance(sprite, BossSpawn):
					sprite.image = pygame.transform.scale(aux, (240, 240))
				else:
					sprite.image = pygame.transform.scale(aux, (64, 64))
				offset_pos = ((sprite.rect.topleft[0] - self.offset.x) * self.zoom_factor,
					(sprite.rect.topleft[1] - self.offset.y) * self.zoom_factor)
				self.display_surface.blit(sprite.image, offset_pos)
				sprite.image = aux
			else:
				offset_pos = ((sprite.rect.topleft[0] - self.offset.x) * self.zoom_factor,
					(sprite.rect.topleft[1] - self.offset.y) * self.zoom_factor)
				self.display_surface.blit(sprite.image, offset_pos)