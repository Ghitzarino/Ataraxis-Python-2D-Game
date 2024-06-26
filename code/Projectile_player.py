import pygame

class Projectile_player(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.direction = player.status.split('_')[0]
        self.dir_vect = pygame.math.Vector2()
        self.choice = player.choice
        self.kill_count = 0
        self.isKilled = 0

        if self.choice == 'Knight':
            self.image = pygame.Surface((16,16), pygame.SRCALPHA, 32).convert_alpha()

            if self.direction == 'right':
                self.rect = self.image.get_rect(topleft = player.rect.topright + pygame.math.Vector2(0,0))
            elif self.direction == 'left':
                self.rect = self.image.get_rect(topright = player.rect.topleft + pygame.math.Vector2(0,0))
            elif self.direction == 'up':
                self.rect = self.image.get_rect(bottomleft = player.rect.topleft + pygame.math.Vector2(0,0))
            elif self.direction == 'down':
                self.rect = self.image.get_rect(topleft = player.rect.bottomleft + pygame.math.Vector2(0,0))

            self.hitbox = self.rect

        elif self.choice == 'Archer':
            self.speed = 3

            self.image = pygame.image.load('../graphics/arrow/arrow_{}.png'.format(self.direction)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (44, 44))

            if self.direction == 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-2,18))
            elif self.direction == 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(35,18))
            elif self.direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(17,35))
            elif self.direction == 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(17,-2))

            scaled_width = int(self.rect.width * player.zoom_factor)
            scaled_height = int(self.rect.height * player.zoom_factor)
            self.rect = pygame.Rect(self.rect.x, self.rect.y, scaled_width, scaled_height)

            self.hitbox = self.rect.inflate(-20, -20)
        
        elif self.choice == 'Mage':
            self.speed = 2

            self.image = pygame.image.load('../graphics/magic/magic_{}.png'.format(self.direction)).convert_alpha()
            self.image = pygame.transform.scale(self.image, (44, 44))

            if self.direction == 'right':
                self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-4,18))
            elif self.direction == 'left':
                self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(37,18))
            elif self.direction == 'up':
                self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(19,37))
            elif self.direction == 'down':
                self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(13,-4))

            scaled_width = int(self.rect.width * player.zoom_factor)
            scaled_height = int(self.rect.height * player.zoom_factor)
            self.rect = pygame.Rect(self.rect.x, self.rect.y, scaled_width, scaled_height)

            self.hitbox = self.rect.inflate(0, -2)    


    def update(self):
        if self.choice == 'Knight':
            if self.kill_count >= 3:
                self.isKilled = 1
                self.kill()
            pass
        else:
            if self.direction == 'right':
                self.dir_vect.x = 1
            elif self.direction == 'left':
                self.dir_vect.x = -1
            elif self.direction == 'up':
                self.dir_vect.y = -1
            elif self.direction == 'down':
                self.dir_vect.y = 1

            self.hitbox.x += self.dir_vect.x * self.speed
            self.hitbox.y += self.dir_vect.y * self.speed
            self.rect.center = self.hitbox.center
        if self.choice == 'Archer' and self.kill_count >= 1:
            self.isKilled = 1
            self.kill()
        elif self.choice == 'Mage' and self.kill_count >= 1:
            self.isKilled = 1
            self.kill()