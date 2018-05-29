import pygame
from tiles import *
from matrix import *
from textures import *
from gui import *
from settings import *
from user import *
import levels
import random


class Defaults:
    pygame.init()
    window = pygame.display.set_mode(G.WINDOW)
    pygame.display.set_caption("Game")
    clock = pygame.time.Clock()

    Texture("BLACK").bulk("")

    mouse = pygame.mouse.get_pos()
    pressed = pygame.key.get_pressed()
    event_list = []


class Poke(Defaults):
    def __init__(self):
        self.player = Player()
        self.player.spawn([3, 3])
        self.level = levels.importer("maps/cave.map", G.size)

        self.move = [0, 0]

        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            self.window.fill((0, 0, 0))

            for x, y, tile in self.level.all():
                tile.blit(x, y, G.TILE_SIZE, self.move)

            self.player.blit(G.PLAYER_SIZE, self.move)

            Group.all_draw("")

            self.event_list = pygame.event.get()
            self.mouse = pygame.mouse.get_pos()

            self.player.event(self.event_list)
            Group.all_event("", self.mouse, self.event_list)

            if Group.no_events():
                for event in self.event_list:
                    if event.type == pygame.QUIT:
                        self.running = False

            pygame.display.update()


if __name__ == "__main__":
    p = Poke()
