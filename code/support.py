from csv import reader
import pygame
from settings import *
from os import walk

def import_csv_layout(path):
    terrain_map = []
    with open(path) as map:
        level = reader(map, delimiter= ',')
        for row in level:
            terrain_map.append(list(row))
        return terrain_map

def import_cut_graphics(path, zoom_factor = 1.0):
    surface = pygame.image.load(path).convert_alpha()
    tile_num_x = int(surface.get_size()[0] / TILESIZE)
    tile_num_y = int(surface.get_size()[1] / TILESIZE)

    cut_tiles = []
    for row in range(tile_num_y):
        for col in range(tile_num_x):
            x = col * TILESIZE
            y = row * TILESIZE
            new_surf = pygame.Surface((TILESIZE, TILESIZE), flags= pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, TILESIZE, TILESIZE))
            new_surf = pygame.transform.scale(new_surf, (int(TILESIZE * zoom_factor), int(TILESIZE * zoom_factor)))

            cut_tiles.append(new_surf)

    return cut_tiles

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            if 'fireball' in full_path:
                image_surf = pygame.transform.scale(image_surf, (64, 32))
            elif 'raccoon' in full_path:
                image_surf = pygame.transform.scale(image_surf, (64, 64))
            else:
                image_surf = pygame.transform.scale(image_surf, (16, 16))

            surface_list.append(image_surf)

    return surface_list