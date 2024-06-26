import pygame
from settings import *
from support import import_csv_layout
from game_data import level_1

class Room():
    def __init__(self, details, index):
        self.x_list = []
        self.y_list = []
        self.length_list = []
        self.height_list = []
        if index == 'Boss':
            self.room_index = 21
        else:
            self.room_index = int(index)
        string  = 'room' + index
        self.room_sprites_layout = import_csv_layout(level_1[string])
        self.sprite_group = pygame.sprite.Group()
        self.obstacle_group = pygame.sprite.Group()
        self.playerIn = 0
        self.enemy_count = 0

        for room_details in details:
            x, y, length, height = room_details
            self.x_list.append(x)
            self.y_list.append(y)
            self.length_list.append(length)
            self.height_list.append(height)

    def isIn(self, x, y):
        n = len(self.x_list)
        for i in range(n):
            if (self.x_list[i] + 1.5) * TILESIZE - 1 <= x < (self.x_list[i] + self.length_list[i] - 1.5) * TILESIZE + 1 and (self.y_list[i] + 1.5) * TILESIZE - 4 <= y < (self.y_list[i] + self.height_list[i] - 1.5) * TILESIZE + 7:
                
                return self.room_index
        return -1