import pygame


class teleportation_objects:
    def __init__(self, surface, position):
        self.rect = surface.get_rect(center=position)
        self.x = position[0]
        self.y = position[1]
        self.surface = surface

    def get_rect(self):
        return self.rect


class Tomato:
    def __init__(self, surface, positionX, positionY):
        self.surface = surface
        self.positionX = positionX
        self.positionY = positionY
        self.rect = surface.get_rect(center=(self.positionX, self.positionY))

    def get_rect(self):
        return self.rect


class Game_over:
    def __init__(self):
        self.game_over_animation = []
        self.frames = [0]
        for i in range(1, 11):
            self.game_over_animation.append(
               pygame.image.load("images/game_over_frames/game_over {}.png".format(i)))
            self.frames.append(i - 1)
        self.current_sprite = 0
        self.animation_speed = 0.2
        self.image = 0
        self.rect = self.game_over_animation[self.image].get_rect(topleft=(0, 0))

    def update(self):
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.frames):
            self.current_sprite = 0
        self.image = self.frames[int(self.current_sprite)]
        return self.game_over_animation[self.image]


game_over = Game_over()
is_brute = False
possibly_healing = False
eaten = False
tp_object = 0
tp_points_placement_x = 0
tp_points_placement_y = 0
ladder = 0
hole = 0
trophy = 0
already_added = False

