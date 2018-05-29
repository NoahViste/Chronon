import pygame
from tiles import *
from matrix import *
from textures import *
from gui import *
from settings import *
from user import *
import levels
import random
from main import Defaults


class Editor(Defaults):
    def __init__(self):
        G.TILE_SIZE = TILE_SIZE
        Defaults.size = pygame.Rect(0, 0, *G.TILE_SIZE)

        self.level = Grid((10, 8), Tile())
        for i in self.level.all():
            i[2].set(Texture("BLACK", rect=G.size))
        self.move = [80, 80]
        self.mouse_move = False

        self.selected = ("WHITE", 0)

        self.group = "Editor"

        self.ui_input = Input((0, 1, 120, 30), self.group, text="Map name")
        self.ui_save = Button((120, 1, 80, 30), self.group, self.save, text="Save")
        self.ui_load = Button((200, 1, 80, 30), self.group, text="Load")
        self.ui_new = Button((280, 1, 80, 30), self.group, text="New")
        self.ui_texture = Button((360, 1, 120, 30), self.group, text="Textures")
        self.ui_settings = Button((480, 1, 120, 30), self.group, text="Settings")
        self.ui_selected = Display((600, 1, 240, 30), self.group)
        self.ui_selected.pointer("text", self, "selected")

        self.TEXTURE_CLOSE = None
        self.LOAD_CLOSE = None

        self.ov_textures = None
        self.overlay_textures()
        self.ov_settings = None
        self.overlay_settings()
        self.ov_load = None
        self.ov_load_scroll = None
        self.overlay_load()
        self.ov_new = None
        self.overlay_new()

        self.ui_texture.set_func(self.ov_textures.toggle_visible)
        self.ui_settings.set_func(self.ov_settings.toggle_visible)
        self.ui_load.set_func(self.ov_load.toggle_visible)
        self.ui_new.set_func(self.ov_new.toggle_visible)

        self.running = True
        self.loop()

    def save(self):
        file = self.ui_input.get_value() + G.MAP_EXTENSION

        levels.exporter(self.level, "maps/" + file)

        b = Button((0, 40, 260, 30), "", self.select_map(file), text=file)
        b.set_color("LIGHTESTGREY")
        self.ov_load_scroll.add_line(b)

    def loop(self):
        while self.running:
            self.draw()
            self.event()
            pygame.display.update()

    def draw(self):
        self.window.fill(C["LIGHTGREY"])

        for x, y, tile in self.level.all():
            tile.blit(x, y, G.TILE_SIZE, self.move)

        Group.all_draw(self.group)

    def event(self):
        self.event_list = pygame.event.get()
        self.mouse = pygame.mouse.get_pos()
        self.pressed = pygame.key.get_pressed()

        Group.all_event(self.group, self.mouse, self.event_list)

        if Group.no_events():
            for event in self.event_list:
                if event.type == pygame.QUIT:
                    self.running = False

                if self.pressed[pygame.K_SPACE] and pygame.mouse.get_pressed()[0]:
                    if not self.mouse_move:
                        self.mouse_move = self.mouse
                    self.move[0] -= self.mouse_move[0] - self.mouse[0]
                    self.move[1] -= self.mouse_move[1] - self.mouse[1]

                    self.mouse_move = self.mouse
                    continue
                else:
                    self.mouse_move = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.ov_textures.toggle_visible()

                    if event.key == pygame.K_e:
                        G.TILE_SIZE = (32, 32)
                        Defaults.size = pygame.Rect(0, 0, *G.TILE_SIZE)
                        for i in self.level.all():
                            i[2].rescale(G.size)

                if pygame.mouse.get_pressed()[0]:
                    try:
                        tile = self.level.get(*Tile.grid_mouse(G.TILE_SIZE, self.level.get_size(), self.move))

                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            tile.add(Texture(*self.selected, G.size))

                        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                            tile.collision = True

                        else:
                            tile.set(Texture(*self.selected, G.size))

                    except TypeError:
                        print("Mouse outside grid")

                if pygame.mouse.get_pressed()[2]:
                    try:
                        tile = self.level.get(*Tile.grid_mouse(G.TILE_SIZE, self.level.get_size(), self.move))

                        if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                            tile.add(Texture(*self.selected, G.size))

                        elif pygame.key.get_mods() & pygame.KMOD_CTRL:
                            tile.collision = False

                        else:
                            tile.set(Texture(*G.DEFAULT_TEXTURE, G.size))

                    except TypeError:
                        print("Mouse outside grid")

                if pygame.mouse.get_pressed()[1]:
                    try:
                        tile = self.level.get(*Tile.grid_mouse(G.TILE_SIZE, self.level.get_size(), self.move))

                        self.selected = tile.get_image()[0].get_name()

                    except TypeError:
                        print("Mouse outside grid")

    def select_texture(self, name, position):
        def nested():
            self.selected = (name, position)
            if self.TEXTURE_CLOSE.get_value(): self.ov_textures.toggle_visible()
        return nested

    def select_map(self, name):
        def nested():
            self.level = levels.importer("maps/" + name, G.size)
            if self.LOAD_CLOSE.get_value(): self.ov_load.toggle_visible()
        return nested

    def create_map(self, width, height):
        def nested():
            self.level = Grid((width.get_value(), height.get_value()), Tile())
            for i in self.level.all():
                i[2].set(Texture(*G.DEFAULT_TEXTURE, rect=G.size))
        return nested

    def overlay_textures(self):
        ov = Overlay((100, 100, 610, 400), self.group, window_name="Textures")
        scroll = Scroll((10, 40, 590, 350), "")

        l = []
        for sheet in Texture.native:
            for i in range(len(Texture.native[sheet])):
                b = Button((0, 0, 40, 40), "", self.select_texture(sheet, i))
                b.set_color(Texture(sheet, i), Texture(sheet, i))
                l.append(b)
                if not i % 14:
                    scroll.add_line(*l)
                    l = []
        ov.add(scroll)
        ov.add_children(*scroll.loop_all())

        ov.toggle_visible()
        self.ov_textures = ov

    def overlay_settings(self):
        ov = Overlay((100, 100, 300, 400), self.group, window_name="Settings")

        d = Display((10, 40, 280, 30), "", text="Close texture after select", outline=-1)
        d.align_text("left", (10, 0))
        d.set_color("LIGHTESTGREY")
        self.TEXTURE_CLOSE = Tick((267, 48, 15, 15), "", start_enabled=True)

        d2 = Display((10, 80, 280, 30), "", text="Close load map after select", outline=-1)
        d2.align_text("left", (10, 0))
        d2.set_color("LIGHTESTGREY")
        self.LOAD_CLOSE = Tick((267, 88, 15, 15), "", start_enabled=True)

        d3 = Display((10, 120, 280, 30), "", text="Grid thickness", outline=-1)
        d3.align_text("left", (10, 0))
        d3.set_color("LIGHTESTGREY")
        s = Slider((160, 120, 100, 30), "", [-1, 1, 2, 3], outline=-1)
        d4 = Display((260, 120, 30, 30), "", text="", outline=-1)
        d4.pointer("text", s, "current_value")
        d4.pointer("outline", s, "current_value", Tile)

        d5 = Display((10, 160, 280, 30), "", text="Show tile info", outline=-1)
        d5.align_text("left", (10, 0))
        d5.set_color("LIGHTESTGREY")
        t = Tick((267, 168, 15, 15), "", start_enabled=True)
        t.pointer("dev", t, "ticked", Tile)

        ov.add(d, d2, d3, s, s.pull, d4, d5, t, self.TEXTURE_CLOSE, self.LOAD_CLOSE)

        ov.toggle_visible()
        self.ov_settings = ov

    def overlay_load(self):
        ov = Overlay((100, 100, 300, 400), self.group, window_name="Load Map")
        scroll = Scroll((10, 40, 280, 350), "")

        for file in levels.list_all("maps/"):
            b = Button((0, 40, 260, 30), "", self.select_map(file), text=file)
            b.set_color("LIGHTESTGREY")
            scroll.add_line(b)

        ov.add(scroll)
        ov.add_children(*scroll.loop_all())

        ov.toggle_visible()
        self.ov_load = ov
        self.ov_load_scroll = scroll

    def overlay_new(self):
        ov = Overlay((100, 100, 300, 160), self.group, window_name="New map")

        d = Display((10, 40, 280, 30), "", text="Map width", outline=-1)
        d.align_text("left", (10, 0))
        d.set_color("LIGHTESTGREY")
        i = Input((190, 40, 100, 30), "", int_only=True, max_length=2)

        d2 = Display((10, 80, 280, 30), "", text="Map height", outline=-1)
        d2.align_text("left", (10, 0))
        d2.set_color("LIGHTESTGREY")
        i2 = Input((190, 80, 100, 30), "", int_only=True, max_length=2)

        b = Button((10, 120, 280, 30), "", self.create_map(i, i2), text="Create")

        ov.add(d, i, d2, i2, b)

        ov.toggle_visible()
        self.ov_new = ov


if __name__ == "__main__":
    e = Editor()
