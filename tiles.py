import pygame
from settings import *
import math


class Tile:
    window = pygame.display.set_mode((1, 1))
    outline = -1
    dev = False

    def __init__(self, *args):
        self.image = [*args]
        self.collision = False

    def blit(self, x, y, tile_size, move=(0, 0)):
        # Pixels on screen coordinates
        px = x * tile_size[0] + move[0]
        py = y * tile_size[1] + move[1]

        for image in self.image:
            self.window.blit(image(), (px, py))

        pygame.draw.rect(self.window, C["BLACK"], (px, py, *tile_size), self.outline)

        if self.dev:
            if self.collision:
                pygame.draw.rect(self.window, C["RED"], (px, py, *tile_size), 4)

    @staticmethod
    def grid_mouse(tile_size, grid_size, move):
        mouse = pygame.mouse.get_pos()
        # We "remove" the margin
        nx, ny = mouse[0]-move[0], mouse[1]-move[1]
        # Tests whether or not the mouse is within the grid
        if 0 <= nx < tile_size[0] * grid_size[0] and 0 <= ny < tile_size[1] * grid_size[1]:
            return math.trunc(nx / tile_size[0]), math.trunc(ny / tile_size[1])

    def rescale(self, size):
        for tex in self.image:
            tex.rescale(size)

    def set(self, *args):
        self.image = [*args]

    def add(self, *args):
        self.image.extend(args)

    def get_image(self):
        return self.image
