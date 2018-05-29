import pygame
from main import Defaults
from gui import *
from textures import *
import levels
import editor


class Mainmenu(Defaults):
    def __init__(self):
        G.set_size((G.WINDOW[0]//16, G.WINDOW[1]//9))
        self.level = levels.importer("maps/mainmenu.map", G.size)

        self.group = "Menu"

        y = G.WINDOW[1] // 10
        y2 = y//2
        x = G.WINDOW[0] // 4
        x2 = x//2

        self.ui_new = Button((2*x-x2, 8*y-y2, 200, 50), self.group, text="New Game", outline=-1)
        self.ui_new.set_color(Texture("s_ui", 0), Texture("s_ui", 1), Texture("s_ui", 2), c_font="WHITE")
        self.ui_load = Button((2*x-x2, 9*y-y2, 200, 50), self.group, text="Load Game", outline=-1)
        self.ui_load.set_color(Texture("s_ui", 0), Texture("s_ui", 1), Texture("s_ui", 2), c_font="WHITE")
        self.ui_options = Button((x-x2, 8*y-y2, 200, 50), self.group, text="Options", outline=-1)
        self.ui_options.set_color(Texture("s_ui", 0), Texture("s_ui", 1), Texture("s_ui", 2), c_font="WHITE")
        self.ui_credits = Button((x-x2, 9*y-y2, 200, 50), self.group, text="Credits", outline=-1)
        self.ui_credits.set_color(Texture("s_ui", 0), Texture("s_ui", 1), Texture("s_ui", 2), c_font="WHITE")
        self.ui_editor = Button((3*x-x2, 8*y-y2, 200, 50), self.group, self.editor_func, text="Editor", outline=-1)
        self.ui_editor.set_color(Texture("s_ui", 0), Texture("s_ui", 1), Texture("s_ui", 2), c_font="WHITE")
        self.ui_quit = Button((3*x-x2, 9*y-y2, 200, 50), self.group, self.quit, text="Quit", outline=-1)
        self.ui_quit.set_color(Texture("s_ui", 0), Texture("s_ui", 1), Texture("s_ui", 2), c_font="WHITE")

        self.running = True
        self.loop()

    def loop(self):
        while self.running:
            self.window.fill((0, 0, 0))

            for x, y, tile in self.level.all():
                tile.blit(x, y, G.TILE_SIZE)

            Group.all_draw(self.group)

            self.event_list = pygame.event.get()
            self.mouse = pygame.mouse.get_pos()

            Group.all_event(self.group, self.mouse, self.event_list)

            if Group.no_events():
                for event in self.event_list:
                    if event.type == pygame.QUIT:
                        self.running = False

            pygame.display.update()

    def quit(self):
        self.running = False

    def editor_func(self):
        G.reset()
        editor.Editor()
        G.set_size((G.WINDOW[0] // 16, G.WINDOW[1] // 9))


if __name__ == "__main__":
    m = Mainmenu()
