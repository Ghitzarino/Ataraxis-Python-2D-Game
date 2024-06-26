import pygame
from settings import * 

class UI:
	def __init__(self, type):
		
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font(UI_FONT,UI_FONT_SIZE)

		self.health_bar_rect = pygame.Rect(60,10,HEALTH_BAR_WIDTH,BAR_HEIGHT)
		self.energy_bar_rect = pygame.Rect(10,34,ENERGY_BAR_WIDTH,BAR_HEIGHT)
		if (type == 'Knight'):
			self.type = 'sword/sword_'
		elif type == 'Archer':
			self.type = 'bow/bow_'
		elif type == 'Mage':
			self.type = 'wand/wand_'
		self.type = '../graphics/' + self.type
		self.character_image = pygame.image.load(self.type + 'on.png').convert_alpha()
		self.character_image = pygame.transform.scale(self.character_image, (50, 50))

	def show_bar(self,current,max_amount,bg_rect,color):
		pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)

		ratio = current / max_amount
		current_width = bg_rect.width * ratio
		current_rect = bg_rect.copy()
		current_rect.width = current_width

		pygame.draw.rect(self.display_surface,color,current_rect)
		pygame.draw.rect(self.display_surface,UI_BORDER_COLOR,bg_rect,3)

	def draw_character(self):
		x = 0
		y = self.display_surface.get_height() - 50
		self.display_surface.blit(self.character_image, (x, y))


	

	def display(self,player, ability):
		if player.health > player.max_health:
			self.show_bar(player.max_health,player.max_health,self.health_bar_rect,HEALTH_COLOR)
		else:
			self.show_bar(player.health,player.max_health,self.health_bar_rect,HEALTH_COLOR)
		string = self.type
		if ability == False:
			string += 'on.png'
		else:
			string += 'off.png'
		self.character_image = pygame.image.load(string).convert_alpha()
		self.character_image = pygame.transform.scale(self.character_image, (50, 50))
		self.draw_character()