import pygame


class Sonic(pygame.sprite.Sprite):
    def __init__(self, x, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = self.image.get_rect(center=(x, 0))

    def update(self, *args):
        pygame.image.load('sprites/sonic_sprites_1_1.png')