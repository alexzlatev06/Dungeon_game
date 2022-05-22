import pygame
from levels import *


# I use this class in order to create tiles that will later create the full levels
# the tile type is just the texture that I am using for each tile(grass, sand, wall etc.)
# there is also a 'is_wall' and 'is_dangerous' bool variables
# that I use to separate normal tiles from wall and lava tiles
# the difference is that the player collides with the wall types adn takes damage from the 'dangerous tiles'
# and just walks over the other ones
class Tile(pygame.sprite.Sprite):
    def __init__(self, position, tile_type):
        super().__init__()
        self.image = pygame.image.load(tile_type)
        self.rect = self.image.get_rect(topleft=position)
        self.width = 0
        self.height = 0
        self.is_wall = False
        self.is_dangerous = False

# I use update in order to move the tiles inside and outside the screen, because pygame has no camera
# by moving the tiles I create the illusion that the player is actually moving around the map
# the movement argument comes from the run function from the 'Level' class -
# it gives me the x and y parameters that I use to move every tile
    def update(self, movement):
        self.rect.x += movement[0]
        self.rect.y += movement[1]

    def get_rect(self):
        if self.is_dangerous:
            self.rect.width = 10
            self.rect.height = 10
        return self.rect


# this class draws my level on the screen by using the 'level_info'
# 'level info' is a list that has certain information that I use in order to know which tile to draw on the screen
class Level:
    def __init__(self, level_info, screen):
        self.screen = screen
        self.level_info = level_info
        self.start_x = 0
        self.start_y = 0
        self.level_creation(level_info)

# 'level info' is a list that is filled with strings that are filled with capital letters
# each string is a 'row' and each letter is a 'colum'
# after creating a tile I add it to a 'tiles'
# I also check if a tile is a wall so I know if I need to collide with it
# and which are the coordinates of the final tile so I know the width and height of the level
    def level_creation(self, level_info):
        for row_index, row in enumerate(level_info):
            for colum_index, cell in enumerate(row):
                if cell == 'G':
                    tile = Tile((colum_index * tile_size, row_index * tile_size), "images/grass.png")
                    tiles.add(tile)
                elif cell == 'S':
                    tile = Tile((colum_index * tile_size, row_index * tile_size), "images/sand.png")
                    tiles.add(tile)
                elif cell == 'O':
                    tile = Tile((colum_index * tile_size, row_index * tile_size), "images/rocky_ground.png")
                    tiles.add(tile)
                elif cell == "B":
                    tile = Tile((colum_index * tile_size, row_index * tile_size), "images/black_ground.png")
                    tiles.add(tile)
                elif cell == 'W':
                    tile = Tile((colum_index * tile_size, row_index * tile_size), "images/wall.png")
                    tile.is_wall = True
                    tiles.add(tile)
                elif cell == 'L':
                    tile = Tile((colum_index * tile_size, row_index * tile_size), "images/lava.png")
                    tile.is_dangerous = True
                    tiles.add(tile)
                elif cell == "e":
                    self.width = (colum_index - 1) * tile_size
                    self.height = (row_index - 1) * tile_size

# this function draws the level on the screen and moves each tile by the parameters that are given,
# making it look like the whole level moves
    def run(self, world_movement):
        tiles.update(world_movement)
        tiles.draw(self.screen)


tiles = pygame.sprite.Group()
