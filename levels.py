from tiles import Tile
from textures import Texture
from matrix import Grid
from settings import *
import os


def exporter(grid, name):
    with open(name, "w+") as file:
        file.write("{0},{1}\n".format(grid.width, grid.height))
        for tile in grid.all():
            file.write("|,{0}\n".format(int(tile[2].collision)))
            for image in tile[2].image:
                file.write("{0},{1}\n".format(image.name, image.position))
            file.write("/\n")


def importer(name, texture_size):
    with open(name, "r") as file:
        lines = file.readlines()
        size = lines[0].split(",")
        size = int(size[0]), int(size[1])
        grid = Grid(size)

        useless = None
        collision = False

        x, y = 0, 0
        state = "new"
        for line in lines[1:]:
            if "/" in line:
                state = "new"
                x += 1
                if x >= size[0]:
                    y += 1
                    x = 0
                continue

            if "|" in line:
                useless, collision = line.split(",")
                continue

            if state == "new":
                texture, position = line.split(",")
                tile = Tile(Texture(texture, int(position), texture_size))
                tile.collision = bool(int(collision))
                grid.put(x, y, tile)
                state = "added"
                continue

            if state == "added":
                texture, position = line.split(",")
                grid.get(x, y).add(Texture(texture, int(position), texture_size))

    return grid


def list_all(folder):
    all_files = os.listdir(folder)
    filtered_files = []

    for file in all_files:
        if G.MAP_EXTENSION in file:
            filtered_files.append(file)

    return filtered_files
