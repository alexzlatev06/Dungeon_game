import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, player_x, player_y):
        super().__init__()
        test.assertEqual(isinstance(player_x, int), True, "player_x has to be an integer")
        test.assertEqual(isinstance(player_y, int), True, "player_y has to be an integer")
        self.playerX = player_x
        self.playerY = player_y
        self.health = 3
        self.player_movement = []
        self.looking_towards = " "
        self.frames = [0]
        self.current_sprite = 0
        # here we load all the images from the folder and put them into a list
        # the current frame which is shown on screen depends on the 'current_sprite' which is a number that gets updated
        # in the update function(the current sprite is the index of the frame that we want to take from the list)
        # the current rect of the player is dependant on the rect of the image(in most cases the same)
        # the frames list ,meanwhile, holds all index of all the frames that we currently want to use
        # (you will see this also in the enemy classes)
        for i in range(1, 51):
            self.player_movement.append(pygame.image.load("images/hero_movement/hero {}.png".format(i)))
        self.image = self.player_movement[self.current_sprite]
        self.rect = self.image.get_rect(center=(self.playerX, self.playerY))
        self.animation_speed = 0
        self.player_speed = pygame.math.Vector2(self.playerX, self.playerY)
        self.is_moving = False

# this function simply takes input from the keyboard and depending on the key that is pressed
# moves the player in a certain direction and also changes the frames that will be shown
# 'looking_towards' is used to help the camera movement function work and also help the
# goblin brute activate it's attacking animation
    def movement(self):
        key = pygame.key.get_pressed()
        if key and self.is_moving:
            self.animation_speed = 0.25
            if key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_UP] and not key[pygame.K_DOWN]:
                self.frames = [20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
                self.looking_towards = "left"
                self.player_speed.x = -5
            elif key[pygame.K_RIGHT] and not key[pygame.K_LEFT] and not key[pygame.K_UP] and not key[pygame.K_DOWN]:
                self.frames = [40, 41, 42, 43, 44, 45, 46, 47, 48, 49]
                self.looking_towards = "right"
                self.player_speed.x = 5
            elif key[pygame.K_UP] and not key[pygame.K_LEFT] and not key[pygame.K_RIGHT] and not key[pygame.K_DOWN]:
                self.frames = [30, 31, 32, 33, 34, 35, 36, 37, 38, 39]
                self.looking_towards = "up"
                self.player_speed.y = -5
            elif key[pygame.K_DOWN] and not key[pygame.K_LEFT] and not key[pygame.K_UP] and not key[pygame.K_RIGHT]:
                self.frames = [10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
                self.looking_towards = "down"
                self.player_speed.y = 5
        else:
            self.player_speed.x = 0
            self.player_speed.y = 0
            self.animation_speed = 0.02
            if self.looking_towards == "left":
                self.frames = [3, 4, 5]
            elif self.looking_towards == "right":
                self.frames = [7, 8, 9]
            elif self.looking_towards == "up":
                self.frames = [6]
            elif self.looking_towards == "down":
                self.frames = [0, 1, 2]
            else:
                self.frames = [0, 1, 2]
        return self.frames

# update calls the player movement function and changes the player's coordinates accordingly
# the animation speed here decides how fast the player cycle's through his current frames
# the frames make sure that the 'current_sprite' doesn't become bigger than the last index of the list
# 'current_sprite' gets made into an int at the end, because of the high chance of it being a float number beforehand
    def update(self):
        Player.movement(self)
        self.playerX += self.player_speed.x
        self.playerY += self.player_speed.y
        self.current_sprite += self.animation_speed
        if self.current_sprite >= len(self.frames):
            self.current_sprite = 0
        return pygame.transform.scale(self.player_movement[self.frames[int(self.current_sprite)]], (80, 80))

# returning the rectangle that surrounds the player
# it is used later on in order to detect collision between the player and enemies/walls
    def get_rect(self):
        self.rect = self.image.get_rect(topleft=(self.playerX, self.playerY))
        self.rect.width = 70
        self.rect.height = 70
        return self.rect


player = Player(50, 50)
