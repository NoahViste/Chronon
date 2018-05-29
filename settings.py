import pygame

TILE_SIZE = (64, 64)


class G:
    # Window stuff:
    WINDOW = (1600, 900)
    FONT = "times new roman"
    FONT_SIZE = 20
    GROUP = "maker"
    TILE_SIZE = (64, 64)
    size = pygame.Rect(0, 0, *TILE_SIZE)
    PLAYER_SIZE = (64, 64)
    PLAYER_TEXTURE = "a_char"
    DEFAULT_TEXTURE = ["BLACK", 0]

    MAP_EXTENSION = ".map"

    @staticmethod
    def reset():
        G.set_size(TILE_SIZE)

    @staticmethod
    def set_size(size):
        G.TILE_SIZE = size
        G.size = pygame.Rect(0, 0, *size)


# Colors:
C = {}
C["RED"] = (255, 0, 0)
C["GREEN"] = (0, 255, 0)
C["BLUE"] = (0, 0, 255)

C["BROWN"] = (125, 80, 35)
C["DARKRED"] = (139, 0, 0)

C["BLACK"] = (0, 0, 0)
C["WHITE"] = (255, 255, 255)

C["GREY"] = (127, 127, 127)
C["DARKGREY"] = (55, 55, 55)
C["LIGHTGREY"] = (180, 180, 180)
C["LIGHTERGREY"] = (210, 210, 210)
C["LIGHTESTGREY"] = (230, 230, 230)

# Default object colors
C["canvas"] = (238, 238, 238)
C["main"] = (210, 210, 210)
C["main_trans"] = (0, 0, 0, 125)
C["outline"] = (0, 0, 0)
C["font"] = (0, 0, 0)
C["hover"] = (185, 185, 185)
C["click"] = (145, 145, 145)
C["line"] = (0, 0, 0)
C["topbar"] = (180, 180, 180)
C["exit"] = (139, 0, 0)
C["tick"] = (139, 0, 0)
C["tick_click"] = (210, 210, 210)
