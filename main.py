import pygame
import os.path
import random
from levels import *
from CP import *  # create player
from CE import *  # create enemy
from level_creation import *
from TP_and_healing_object import *

# opening the console and initializing the music commands in python
pygame.init()
pygame.mixer.init()
screen_width = 900
screen_height = 700
running = True
is_game_over = False
fps = 60
clock = pygame.time.Clock()
black_colour = (0, 0, 0)
screen = pygame.display.set_mode((screen_width, screen_height))
# killing_cooldown - a weird name, but a simple use - getting sure that the player doesn't get killed
# in under a second when colliding with an enemy
killing_cooldown = 80
# a variable that we will use in order to determine which level will be on the screen
# and what is going to happen with it
current_level = 1
level = Level(level1, screen)


# a function that determines which frame of the health bar will be on the screen after checking
# the current player health
def health_bar():
    if player.health == 3:
        return pygame.image.load("images/health bar_frames/health bar 1.png")
    elif player.health == 2:
        return pygame.image.load("images/health bar_frames/health bar 2.png")
    elif player.health == 1:
        return pygame.image.load("images/health bar_frames/health bar 3.png")
    else:
        return pygame.image.load("images/health bar_frames/health bar 4.png")


# this function checks if the player is currently colliding with any of the enemies that are on the screen
def taking_damage():
    global is_brute
    for enemy in current_enemies:
        for tile in tiles:
            if pygame.Rect.colliderect(player.get_rect(), enemy.get_rect()):
                if isinstance(enemy, Goblin_brute):
                    is_brute = True
                else:
                    is_brute = False
                return True
            elif pygame.Rect.colliderect(player.get_rect(), tile.get_rect()) and tile.is_dangerous:
                return True
    return False


# a function that checks if the player has collided with a healing item(currently there is only a tomato)
# if that happens and the player isn't on max health than it heals him(increases tha player.health)
def healing():
    global possibly_healing
    global world_movement_x
    global world_movement_y
    global eaten
    if current_level == 3:
        tomato.rect.x += world_movement_x
        tomato.rect.y += world_movement_y
        if pygame.Rect.colliderect(player.get_rect(), tomato.get_rect()) and not eaten:
            if player.health < 3:
                player.health += 1
                eaten = True
                possibly_healing = False


# if the player reaches the end of the screen then this function stops him from leaving it
def collision_with_screen():
    if player.playerX < 30 and player.is_moving:
        player.playerX -= player.player_speed.x
    if player.playerX > screen_width - 100 and player.is_moving:
        player.playerX -= player.player_speed.x
    if player.playerY > screen_height - 100 and player.is_moving:
        player.playerY -= player.player_speed.y
    if player.playerY < 30 and player.is_moving:
        player.playerY -= player.player_speed.y


# if the player collides with a wall than his movement gets stopped which doesn't allow him to leave the level
def collision_with_wall():
    global tiles
    for piece in tiles:
        if piece.is_wall and pygame.Rect.colliderect(player.get_rect(), piece.get_rect()) and player.looking_towards == "right" :
            player.playerX -= player.player_speed.x
        if piece.is_wall and pygame.Rect.colliderect(player.get_rect(), piece.get_rect()) and player.looking_towards == "left":
            player.playerX -= player.player_speed.x
        if piece.is_wall and pygame.Rect.colliderect(player.get_rect(), piece.get_rect()) and player.looking_towards == "up":
            player.playerY -= player.player_speed.y
        if piece.is_wall and pygame.Rect.colliderect(player.get_rect(), piece.get_rect()) and player.looking_towards == "down":
            player.playerY -= player.player_speed.y


# depending on the current level the object that the player has to touch in order to reach the next level
# or win the game changes
def tp_points():
    global tp_object
    global current_level
    if current_level == 1:
        tp_object = cave
    elif current_level == 2:
        tp_object = ladder
    elif current_level == 3:
        tp_object = hole
    elif current_level == 4:
        tp_object = trophy


# after checking the level this function calls the tp_points() function
# in order to assure that the first tp object(the cave) will show on the screen
# after that it resets the player coordinates, destroys the old level, creates the next one,
# changes the tp object and sets to False the 'already_added' bool variable in order for the new enemies to spawn
# if you win it ends the game and assures the the program knows that you won by using a variable
def collision_with_tp_objects():
    global current_level
    global level
    global cave
    global ladder
    global hole
    global trophy
    global tomato
    global already_added
    global possibly_healing
    global is_game_over
    if current_level == 1:
        tp_points()
        if pygame.Rect.colliderect(player.get_rect(), cave.get_rect()):
            player.playerX = 50
            player.playerY = 50
            for piece in tiles:
                piece.kill()
            current_level = 2
            ladder = teleportation_objects(pygame.image.load("images/Ladder.png"), tp_object_cords())
            tp_points()
            level = Level(level2, screen)
            already_added = False
    elif current_level == 2:
        if pygame.Rect.colliderect(player.get_rect(), ladder.get_rect()):
            player.playerX = 50
            player.playerY = 50
            for piece in tiles:
                piece.kill()
            current_level = 3
            hole = teleportation_objects(pygame.image.load("images/Hole.png"), tp_object_cords())
            tomato = Tomato(pygame.image.load("images/Tomatoes.png"), random.randint(150, level.width), random.randint(150, tile_size * 45))
            tp_points()
            possibly_healing = True
            level = Level(level3, screen)
            already_added = False
    elif current_level == 3:
        if pygame.Rect.colliderect(player.get_rect(), hole.get_rect()):
            player.playerX = 50
            player.playerY = 50
            for piece in tiles:
                piece.kill()
            current_level = 4
            trophy = teleportation_objects(pygame.image.load("images/Trophy.png"), tp_object_cords())
            tp_points()
            level = Level(level4, screen)
            already_added = False
        if possibly_healing:
            screen.blit(tomato.surface, (tomato.rect.x, tomato.rect.y))
    elif current_level == 4:
        if pygame.Rect.colliderect(player.get_rect(), trophy.get_rect()):
            is_game_over = True
            current_level = "winner"


# depending on the level it sets the coordinates of the tp objects
# by using the program Tiled I pick a tile from my map than multiply it by the current tile size
# so I can be sure that the tp object doesn't move from it's position too much
def tp_object_cords():
    global tp_points_placement_x
    global tp_points_placement_y
    global level
    if current_level == 1:
        tp_points_placement_x = tile_size * 39
        tp_points_placement_y = tile_size * 34
    elif current_level == 2:
        tp_points_placement_x = tile_size * 7
        tp_points_placement_y = tile_size * 52
    elif current_level == 3:
        tp_points_placement_x = tile_size * 56
        tp_points_placement_y = tile_size * 44
    elif current_level == 4:
        spawn_position = random.randint(1, 3)
        if spawn_position == 1:
            tp_points_placement_x = tile_size * 71
            tp_points_placement_y = tile_size * 4
        elif spawn_position == 2:
            tp_points_placement_x = tile_size * 42
            tp_points_placement_y = tile_size * 41
        elif spawn_position == 3:
            tp_points_placement_x = tile_size * 56
            tp_points_placement_y = tile_size * 40
    return (tp_points_placement_x, tp_points_placement_y)


cave = teleportation_objects(pygame.image.load("images/cave entrance.png"), tp_object_cords())


# whenever the player reaches the end of the screen his movement is stopped by the collision_with_screen function
# which is supported by this function
# this function changes the speed with which the tiles on the map move
# in order to make it look like the player is moving through the map
def camera_movement():
    global world_movement_x
    global world_movement_y
    if player.is_moving:
        if player.playerX > screen_width - 100 and player.is_moving and player.looking_towards == "right":
            world_movement_x = -6
        elif player.playerX < 30 and player.is_moving and player.looking_towards == "left":
            world_movement_x = 6
        else:
            world_movement_x = 0
        if player.playerY > screen_height - 100 and player.is_moving and player.looking_towards == "down":
            world_movement_y = -6
        elif player.playerY < 30 and player.is_moving and player.looking_towards == "up":
            world_movement_y = 6
        else:
            world_movement_y = 0
    else:
        world_movement_x = 0
        world_movement_y = 0
    return (world_movement_x, world_movement_y)


# it simply moves the object inside the level with the speed with which the tiles move
def object_inside_level_movement():
    global tp_object
    global world_movement_x
    global world_movement_y
    tp_object.rect.x += world_movement_x
    tp_object.rect.y += world_movement_y


# the simplest to explain are the 1st and 3rd level
# the game assigns the enemy's position by giving it random coordinates by using the randint() function
# in the 2nd and 4th level I personally chose where the enemy starts and where it turns around
# in the 4th level I also have to choose which enemies will move vertically and which horizontally
# after I have done all of that I add them to 'current enemies' list
# which holds the enemies that are supposed to be on screen currently
# after all of that I make 'already added' True so that the enemies stop being created and added into the list
def current_enemies_creation():
    global current_level
    global screen_width
    global screen_height
    global current_enemies
    global already_added
    if current_level == 1 and not already_added:
        rock_dude = Rock_dude(random.randint(150, level.width), random.randint(150, level.height))
        goblin_dude = Goblin_dude(random.randint(150, level.width), random.randint(150, level.height))
        current_enemies.add(rock_dude)
        current_enemies.add(goblin_dude)
        already_added = True
    elif current_level == 2 and not already_added:
        for enemy in current_enemies:
            enemy.kill()
        spike_dude = Spike_dude(tile_size * 9, tile_size * 18)
        small_spike_guy = Small_spike_dude(tile_size * 17, tile_size * 34)
        spike_dude2 = Spike_dude(tile_size * 9, tile_size * 50)
        spike_dude.starting_point = tile_size * 9
        spike_dude2.starting_point = tile_size * 9
        small_spike_guy.starting_point = tile_size * 17
        spike_dude.turning_around_point = tile_size * 40
        spike_dude2.turning_around_point = tile_size * 40
        small_spike_guy.turning_around_point = tile_size * 36
        current_enemies.add(spike_dude)
        current_enemies.add(small_spike_guy)
        current_enemies.add(spike_dude2)
        already_added = True
    elif current_level == 3 and not already_added:
        for enemy in current_enemies:
            enemy.kill()
        rock_dude2 = Rock_dude(random.randint(150, level.width), random.randint(150, level.height))
        goblin_dude2 = Goblin_dude(random.randint(150, level.width), random.randint(150, level.height))
        murder = Killer(random.randint(150, level.width), random.randint(150, level.height))
        murder2 = Killer(random.randint(150, level.width), random.randint(150, level.height))
        lizard = Lizard(random.randint(150, level.width), random.randint(150, level.height))
        current_enemies.add(rock_dude2)
        current_enemies.add(goblin_dude2)
        current_enemies.add(murder)
        current_enemies.add(murder2)
        current_enemies.add(lizard)
        already_added = True
    elif current_level == 4 and not already_added:
        for enemy in current_enemies:
            enemy.kill()
        spike_dude = Spike_dude(tile_size * 53, tile_size * 9)
        small_spike_guy = Small_spike_dude(tile_size * 31, tile_size * 9)
        spike_dude2 = Spike_dude(tile_size * 4, tile_size * 25)
        spike_dude3 = Spike_dude(tile_size * 6, tile_size * 40)
        small_spike_guy2 = Small_spike_dude(tile_size * 47, tile_size * 48)
        spike_dude4 = Spike_dude(tile_size * 67, tile_size * 45)
        goblin_brute = Goblin_brute(tile_size * 70, tile_size * 6)

        spike_dude.movement = "vertically"
        small_spike_guy.movement = "vertically"
        small_spike_guy2.movement = "vertically"

        spike_dude.starting_point = spike_dude.positionY
        small_spike_guy.starting_point = small_spike_guy.positionY
        spike_dude2.starting_point = spike_dude2.positionX
        spike_dude3.starting_point = spike_dude3.positionX
        small_spike_guy2.starting_point = small_spike_guy2.positionY
        spike_dude4.starting_point = spike_dude4.positionX

        spike_dude.turning_around_point = tile_size * 21
        small_spike_guy.turning_around_point = tile_size * 21
        spike_dude2.turning_around_point = tile_size * 42
        spike_dude3.turning_around_point = tile_size * 27
        small_spike_guy2.turning_around_point = tile_size * 64
        spike_dude4.turning_around_point = tile_size * 77
        current_enemies.add(spike_dude)
        current_enemies.add(small_spike_guy)
        current_enemies.add(spike_dude2)
        current_enemies.add(spike_dude3)
        current_enemies.add(small_spike_guy2)
        current_enemies.add(spike_dude4)
        current_enemies.add(goblin_brute)
        already_added = True
    for enemy in current_enemies:
        screen.blit(pygame.transform.scale(enemy.update(), (70, 70)), (enemy.positionX, enemy.positionY))


# this will be a long one....
# in the case of the 1st and 3rd level I don't stop changing the x and y coordinates of the enemies
# until they don't match the ones of the player
# in level 2 and 4 the enemy's x or y changes
# until it doesn't reach the turning point or return back to the starting point
# the variable turn_around prevents the if statements from overlapping and breaking each other
# the enemies also get affected by the world movement
# depending on the position in which they are heading their animations change
# depending on it's type, the enemy's speed changes
# you might have also noticed that a certain enemy is a little too much for the walls to handle.....
def enemy_movement():
    global current_enemies
    global world_movement_x
    global world_movement_y
    global turn_around
    if current_level == 1 or current_level == 3:
        for enemy in current_enemies:
            if isinstance(enemy, Goblin_dude) or isinstance(enemy, Rock_dude):
                speed = 1
            elif isinstance(enemy, Killer) or isinstance(enemy, Level):
                speed = 2
            enemy.positionX += world_movement_x
            enemy.positionY += world_movement_y
            if enemy.positionX < player.playerX:
                enemy.positionX += speed
                enemy.frames = [0, 1, 2, 3, 4, 5, 6, 7]
            elif enemy.positionX > player.playerX:
                enemy.positionX -= speed
                enemy.frames = [8, 9, 10, 11, 12, 13, 14, 15]
            else:
                enemy.frames = [0]
            if enemy.positionY > player.playerY:
                enemy.positionY -= speed
            elif enemy.positionY < player.playerY:
                enemy.positionY += speed
    elif current_level == 2 or current_level == 4:
        for enemy in current_enemies:
            enemy.positionX += world_movement_x
            enemy.positionY += world_movement_y
            speed = 0
            if isinstance(enemy, Spike_dude):
                speed = 4
            elif isinstance(enemy, Small_spike_dude):
                speed = 5
            if enemy.movement == "horizontally":
                enemy.starting_point += world_movement_x
                enemy.turning_around_point += world_movement_x
                if enemy.positionX <= enemy.turning_around_point and not enemy.turn_around:
                    enemy.positionX += speed
                    enemy.frames = [0, 1, 2, 3, 4, 5, 6, 7]
                elif enemy.positionX >= enemy.starting_point and enemy.turn_around:
                    enemy.positionX -= speed
                    enemy.frames = [8, 9, 10, 11, 12, 13, 14, 15]
                else:
                    enemy.turn_around = True
                if enemy.positionX <= enemy.starting_point and enemy.turn_around:
                    enemy.turn_around = False
            elif enemy.movement == "vertically":
                enemy.starting_point += world_movement_y
                enemy.turning_around_point += world_movement_y
                if enemy.positionY <= enemy.turning_around_point and not enemy.turn_around:
                    enemy.positionY += speed
                    enemy.frames = [0, 1, 2, 3, 4, 5, 6, 7]
                elif enemy.positionY >= enemy.starting_point and enemy.turn_around:
                    enemy.positionY -= speed
                    enemy.frames = [8, 9, 10, 11, 12, 13, 14, 15]
                else:
                    enemy.turn_around = True
                if enemy.positionY <= enemy.starting_point and enemy.turn_around:
                    enemy.turn_around = False
            if isinstance(enemy, Goblin_brute):
                for tile in tiles:
                    if pygame.Rect.colliderect(enemy.get_rect(), tile.get_rect()) and tile.is_wall:
                        tile.kill()
                if enemy.positionX < player.playerX:
                    enemy.positionX += 2.5
                    enemy.frames = [21, 22, 23, 24, 25, 26, 27]
                if enemy.positionX > player.playerX:
                    enemy.positionX -= 2.5
                    enemy.frames = [7, 8, 9, 10, 11, 12, 13]
                if enemy.positionY > player.playerY:
                    enemy.positionY -= 2.5
                    enemy.frames = [0, 1, 2, 3, 4, 5, 6]
                if enemy.positionY < player.playerY:
                    enemy.positionY += 2.5
                    enemy.frames = [14, 15, 16, 17, 18, 19, 20]


# this is THE while cycle in which all the magic happens and all the functions get called
# there is a for loop that checks if you are pressing tha 'close' button
# or pressing any of the arrow keys on your keyboard
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            player.is_moving = False
        elif event.type == pygame.KEYDOWN:
            player.is_moving = True
# in this segment here the game nonstop checks if the player is taking_damage and if he is still alive
# if the player dies than the game ends and a Game over screen pops up
    if taking_damage():
        if killing_cooldown <= 0:
            if is_brute:
                player.health -= 2
            else:
                player.health -= 1
            killing_cooldown = 80
            if player.health <= 0:
                is_game_over = True
    if not is_game_over:
        screen.fill(black_colour)
        level.run(camera_movement())
        collision_with_screen()
        collision_with_wall()
        collision_with_tp_objects()
        screen.blit(tp_object.surface, (tp_object.rect.x, tp_object.rect.y))
        screen.blit(health_bar(), (screen.get_width() - 100, 0))
        current_enemies_creation()
        enemy_movement()
        screen.blit(player.update(), (player.playerX, player.playerY))
        object_inside_level_movement()
        healing()
        killing_cooldown -= 1
        clock.tick(60)
# tha game can obviously end by you losing or winning
# if you lose a Game over screen(that is pretty cool) starts playing
# if you win a You won screen pops up and a really cool music starts playing(pray that the music doesn't break)
    elif is_game_over:
        for enemy in current_enemies:
            enemy.kill()
        if current_level == "winner":
            screen.blit(pygame.transform.scale(pygame.image.load("images/You won.png"), (screen_width, screen_height)),
                        (0, 0))
            pygame.mixer.Sound.play(
                pygame.mixer.Sound(os.path.join("audio", "Austin_Wintory_-_BACHRAM_CSGO_MVP_MUSIC_KIT.mp3")))
        else:
            screen.blit(pygame.transform.scale(game_over.update(), (screen_width, screen_height)),
                        (0, 0))
    pygame.display.update()
pygame.quit()
