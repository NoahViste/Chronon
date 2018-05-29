from settings import *
import pygame
from textures import *


class Player:
    window = pygame.display.set_mode((1, 1))

    def __init__(self):
        self.position = [0, 0]
        self.hidden = True
        self.inventory = {}
        self.rect = pygame.Rect(0, 0, *G.PLAYER_SIZE)
        self.image = Texture(G.PLAYER_TEXTURE, rect=self.rect)

    def spawn(self, position):
        self.hidden = False
        self.position = position

    def despawn(self):
        self.hidden = True

    def blit(self, tile_size, move):
        if not self.hidden:
            # Pixels on screen coordinates
            px = self.position[0] * tile_size[0] + move[0]
            py = self.position[1] * tile_size[1] + move[1]

            self.window.blit(self.image(), (px, py))

    def move(self, dx=0, dy=0):
        self.position[0] += dx
        self.position[1] += dy

    def move_to(self, coordinates):
        self.position = coordinates

    def event(self, event_list):
        for event in event_list:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move(-1)
                if event.key == pygame.K_RIGHT:
                    self.move(1)
                if event.key == pygame.K_UP:
                    self.move(dy=-1)
                if event.key == pygame.K_DOWN:
                    self.move(dy=1)
