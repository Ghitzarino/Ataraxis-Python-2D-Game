import pygame
import sys
from settings import *
from level import Level
from game_data import level_1
import config

class Game:
    def __init__(self,screen):
        pygame.init()
        self.screen = screen
        pygame.display.set_caption('Game IA4')
        self.clock = pygame.time.Clock()
        self.level = None
        self.characters = ['../mg1.jpg', '../mg2.jpg', '../mg3.jpg']
        self.selected_character = None
        self.type_character = None

    def character_selection_menu(self):
        self.background = pygame.image.load('../BckCh.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))

        running = True
        selected_index = 0
        character_surfaces = []
        character_size = (200, 300)

        for character in self.characters:
            surface = pygame.image.load(character)
            surface = pygame.transform.scale(surface, character_size)
            character_surfaces.append(surface)

        character_spacing = 120 
        total_width = character_size[0] * len(self.characters) + character_spacing * (len(self.characters) - 1)
        start_x = (1280 - total_width) // 2

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        selected_index = (selected_index - 1) % len(self.characters)
                    elif event.key == pygame.K_RIGHT:
                        selected_index = (selected_index + 1) % len(self.characters)
                    elif event.key == pygame.K_RETURN:
                        self.selected_character = self.characters[selected_index]
                        if selected_index == 0:
                            self.type_character = 'Archer'
                        elif selected_index == 1:
                            self.type_character = 'Mage'
                        else:
                            self.type_character = 'Knight'
                        running = False

            self.screen.fill((0, 0, 0))
            self.screen.blit(self.background, (0, 0))

            for i, surface in enumerate(character_surfaces):
                x_position = start_x + i * (character_size[0] + character_spacing)
                y_position = (720 - character_size[1]) // 2
                rect = surface.get_rect(topleft=(x_position, y_position))

                border_color = (255, 255, 0) if i == selected_index else (255, 255, 255)
                pygame.draw.rect(self.screen, border_color, rect.inflate(20, 20), 2)
                self.screen.blit(surface, rect)

            pygame.display.flip()
            self.clock.tick(60)


    def run(self):
        self.character_selection_menu()
        self.level = Level(level_1,self.type_character)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        self.level.toggle_menu()

            self.screen.fill(WATER_COLOR)
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.running = True
        self.background = pygame.image.load('../BackgroundMusic.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        self.slider_x, self.slider_y = 50, 100
        self.slider_width, self.slider_height = 200, 30
        self.slider_pos = config.volume * self.slider_width
        self.font = pygame.font.SysFont(None, 36)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.running = False
                if event.key == pygame.K_LEFT:
                    self.slider_pos = max(0, self.slider_pos - 10)
                    self.update_volume()
                if event.key == pygame.K_RIGHT:
                    self.slider_pos = min(self.slider_width, self.slider_pos + 10)
                    self.update_volume()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if self.slider_x <= mouse_x <= self.slider_x + self.slider_width and self.slider_y <= mouse_y <= self.slider_y + self.slider_height:
                    self.slider_pos = max(0, min(mouse_x - self.slider_x, self.slider_width))
                    self.update_volume()

    def update_volume(self):
        volume = self.slider_pos / self.slider_width
        config.volume = volume
        pygame.mixer.music.set_volume(volume)

    def draw(self):
        self.screen.fill((0, 0, 0))
        text = self.font.render("Settings - Press M to return to the main menu", True, (255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text, (50, 50))
        pygame.draw.rect(self.screen, (100, 100, 100), (self.slider_x, self.slider_y, self.slider_width, self.slider_height))
        slider_color = (0, 128, 255)
        pygame.draw.rect(self.screen, slider_color, (self.slider_x + self.slider_pos - 5, self.slider_y - 10, 10, self.slider_height + 20))
        volume_label = self.font.render(f"Volum: {int(self.slider_pos / self.slider_width * 100)}%", True, (255, 255, 255))
        self.screen.blit(volume_label, (self.slider_x + self.slider_width + 10, self.slider_y))

    def run(self):
        while self.running:
            self.handle_events()
            self.draw()
            pygame.display.flip()

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGTH))
        self.background = pygame.image.load('../Background.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGTH))
        self.font = pygame.font.Font(None, 36)
        self.options = ["New Game", "Settings", "Quit"]
        self.selected = 0

    def draw(self):
        self.screen.blit(self.background, (0, 0))
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected else (255, 255, 255)
            label = self.font.render(option, True, color)
            x = (WIDTH - label.get_width()) // 2
            y = (HEIGTH // 2) + 30 * i
            self.screen.blit(label, (x, y))

    def update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected = (self.selected - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected = (self.selected + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        if self.options[self.selected] == "Quit":
                            pygame.quit()
                            sys.exit()
                        elif self.options[self.selected] == "New Game":
                            running = False
                            game = Game(self.screen)
                            game.run()
                        else:
                            settings_menu = SettingsMenu(self.screen)
                            settings_menu.run()

            self.draw()
            pygame.display.update()

if __name__ == '__main__':
    menu = Menu()
    menu.update()
