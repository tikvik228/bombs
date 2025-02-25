import os
import pygame
import sys
import random


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bomb(pygame.sprite.Sprite):

    def __init__(self, *group):
        super().__init__(*group)
        self.image = load_image("bomb.png")
        self.image_boom = load_image("boom.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 500 - self.rect.width)
        self.rect.y = random.randrange(0, 500 - self.rect.height)
        while True:
            passing = True
            for i in group[0]:
                if i != self and self.rect.colliderect(i.rect):
                    self.rect.x = random.randrange(0, 500 - self.rect.width)
                    self.rect.y = random.randrange(0, 500 - self.rect.height)
                    passing = False
            if passing:
                break

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


def main():
    pygame.init()
    size = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("boom them all")
    all_sprites = pygame.sprite.Group()
    for _ in range(40):
        Bomb(all_sprites)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    main()