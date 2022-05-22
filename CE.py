import pygame
from CP import *
from level_creation import *


# the 'Enemy' class sets the basic parameters of an enemy
# the way it works is almost identical to the way the 'Player' class works
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.enemy_animation = []
        self.frames = [0]
        self.current_sprite = 0
        self.animation_speed = 0.06
        self.image = 0

    def update(self):
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.frames):
            self.current_sprite = 0
        self.image = self.frames[int(self.current_sprite)]
        return self.enemy_animation[self.image]

    def get_rect(self):
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))
        return self.rect


# the main difference between this enemy and the others is that the 'Goblin_brute' has an attacking animation
# oh, and it also might be a little bit more powerful than the other enemies in game
# , but don't worry, you won't spot the difference :)
class Goblin_brute(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, goblin_brutes)
        self.positionX = positionX
        self.positionY = positionY
        self.attacking = False
        for i in range(1, 54):
            self.enemy_animation.append(
                pygame.image.load("images/enemy_goblin_frames/enemy_goblin {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))

    def movement(self):
        if self.attacking:
            if player.looking_towards == "left":
                self.frames = [43, 44, 45, 46, 47]
            elif player.looking_towards == "right":
                self.frames = [33, 34, 35, 36, 37]
            elif player.looking_towards == "up":
                self.frames = [38, 39, 40, 41, 42]
            elif player.looking_towards == "down":
                self.frames = [28, 29, 30, 31, 32]


class Rock_dude(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, rock_monsters)
        self.positionX = positionX
        self.positionY = positionY
        self.animation_speed = 0.1
        for i in range(1, 17):
            self.enemy_animation.append(pygame.image.load("images/rock_dude_frames/rock_dude {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))


class Goblin_dude(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, goblins)
        self.positionX = positionX
        self.positionY = positionY
        for i in range(1, 17):
            self.enemy_animation.append(pygame.image.load("images/goblin_dude_frames/goblin dude {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))


# this class and the next one have 4 variables that help me control the movement of the enemy by checking when is
# the time to turn 180 degrees around and move in the other direction
# and if the enemy is supposed to move horizontally or vertically
class Spike_dude(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, spike_monsters)
        self.positionX = positionX
        self.positionY = positionY
        self.animation_speed = 0.1
        self.turn_around = False
        self.starting_point = 0
        self.turning_around_point = 0
        self.movement = "horizontally"
        for i in range(1, 17):
            self.enemy_animation.append(pygame.image.load("images/spike_dude_frames/spike dude {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))


class Small_spike_dude(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, small_spike_monsters)
        self.positionX = positionX
        self.positionY = positionY
        self.animation_speed = 0.1
        self.turn_around = False
        self.starting_point = 0
        self.turning_around_point = 0
        self.movement = "horizontally"
        for i in range(1, 17):
            self.enemy_animation.append(pygame.image.load("images/small_spike_frames/small_spike {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))


class Killer(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, killers)
        self.positionX = positionX
        self.positionY = positionY
        self.animation_speed = 0.09
        for i in range(1, 17):
            self.enemy_animation.append(pygame.image.load("images/murder_frames/murder {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))


class Lizard(Enemy):
    def __init__(self, positionX, positionY):
        super().__init__()
        pygame.sprite.Sprite.__init__(self, lizards)
        self.positionX = positionX
        self.positionY = positionY
        self.animation_speed = 0.09
        for i in range(1, 17):
            self.enemy_animation.append(pygame.image.load("images/lizard_frames/lizard {}.png".format(i)))
            self.frames.append(i - 1)
        self.rect = self.enemy_animation[self.image].get_rect(topleft=(self.positionX, self.positionY))


# here I create a group for each type of enemy and also a 'current_enemies' group that contains all enemies that are
# supposed to be on the screen
goblin_brutes = pygame.sprite.Group()
rock_monsters = pygame.sprite.Group()
spike_monsters = pygame.sprite.Group()
goblins = pygame.sprite.Group()
small_spike_monsters = pygame.sprite.Group()
killers = pygame.sprite.Group()
lizards = pygame.sprite.Group()
current_enemies = pygame.sprite.Group()
