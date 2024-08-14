"""
This module contains the player class and functions related to player movement,collision detection.
"""
import sys
import pygame
from game.utils import load_sprite_sheets,load_level_objects
from game.gui import pause_screen,game_win
from game.config import FPS, PLAYER_VEL, HIT_DELAY, BLOCK_SIZE, screen, level_1, level_2, level_3

def collide(player, objects, dx):
    """
    Check for collision between the player and objects in the game world.

    Args:
        player (_type_): _description_
        objects (_type_): _description_
        dx (_type_): _description_

    Returns:
        
    """
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()

    return collided_object

def handle_move(player, objects):
    """
    Handle player movement based on key presses and collision detection.    
    """
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(player.speed)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(player.speed)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name in {"Spike", "Crub", "Bat"}:
            player.make_hit()
            player.speed = 1  # slow down the player
            break
        player.speed = PLAYER_VEL

def handle_vertical_collision(player, objects, dy):
    """
    Handle vertical collision between the player and objects in the game world.
    """
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0.01:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0.01:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects

class Player(pygame.sprite.Sprite):
    """_summary_

    Returns:
        _type_: _description_
    """
    GRAVITY = 1
    SPRITES = load_sprite_sheets("img", "sonic", 42, 42, True)
    ANIMATION_DELAY = 5 # Delay between sprite changes in frames
    HIT_DELAY = 1000 # Delay between hits in milliseconds

    def __init__(self, x, y, width, height):
        """
        Initialize the player object.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "right"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.last_hit_time = 0
        self.jump_sound = pygame.mixer.Sound("game/assets/sound/jump.wav")
        self.jump_sound.set_volume(0.8)
        self.hold_timer = 0
        self.holding_right = False
        self.speed = 8
        self.sprite = self.SPRITES["idle_right"][0]  # Initialize the sprite attribute

    def jump(self):
        """_summary_
        Returns:
            _type_: _description_
        """
        self.y_vel = -self.GRAVITY * 9
        self.jump_sound.play()
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        """
        Move the player by dx and dy.
        """
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        """
        Make the player hit an object.
        """
        current_time = pygame.time.get_ticks()
        # Check if enough time has passed since the last hit
        if current_time - self.last_hit_time >= self.HIT_DELAY:
            self.hit_count += 1
            hit_sound= pygame.mixer.Sound("game/assets/sound/hit.wav")
            hit_sound.play()
            self.hit = True
            self.last_hit_time = current_time  # Update last hit time

    def move_left(self, vel):
        """
        Move player to the left by vel.
        """
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        """
         Move player to the right by vel.
        """
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        """
        Loop the player's movement and animation.
        """
        keys = pygame.key.get_pressed()

        # Apply gravity to y velocity
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)
        self.fall_count += 1
        self.update_sprite()

        # Handle hit reset after delay
        if self.hit:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_hit_time >= HIT_DELAY:
                self.hit = False
                self.last_hit_time = current_time

        # Determine movement based on key presses
        if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT]:
            self.hold_timer += 1
            if self.hold_timer >= fps * 2:  # Held for 2 seconds
                self.holding_right = True
                self.speed = 16
        else:
            self.hold_timer = 0
            self.holding_right = False
            self.speed = 8

    def landed(self):
        """
        Player has landed on the ground.
        """
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        """
        Player has hit their head on the ceiling.
        """
        #self.count = 0
        self.y_vel *= -3

    def update_sprite(self):
        """
        Update the player sprite based on movement and actions.
        """
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            sprite_sheet = "jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "jump"
        elif self.x_vel == 0:
            sprite_sheet = "idle"
        else:
            sprite_sheet = "sprint" if self.speed == 16 else "run"
        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        """
        Update the player's rect and mask based on the sprite.
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x,offset_y):
        """
        Draw the player on the screen.
        """
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y-offset_y))

    def fall(self,max_fall_distance,offset_x,offset_y):
        """
        Handle player falling below a certain distance threshold.
        """
        if self.rect.y > max_fall_distance or self.rect.y < -max_fall_distance:
            restart_position(self)
            offset_x = 0
            offset_y = 0
            self.fall_count = 0
            self.y_vel = 0
            self.jump_count = 0
            self.make_hit()
            hit_sound = pygame.mixer.Sound("game/assets/sound/hit.wav")
            hit_sound.play()
        return offset_x,offset_y

def update_offset_x(player, offset_x, scroll_area_width, width):
    """
    Update the horizontal offset_x based on player's movement and scroll area width.
    """
    if ((player.rect.right - offset_x >= width - scroll_area_width) and player.x_vel > 0) or (
            (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
        offset_x += player.x_vel
    return offset_x

def update_offset_y(player, offset_y, scroll_area_height, height):
    """
    Update the vertical offset_y based on player's movement and scroll area height.
    """
    if ((player.rect.bottom - offset_y >= height - scroll_area_height) and player.y_vel > 0) or (
            (player.rect.top - offset_y <= scroll_area_height +200) and player.y_vel < 0):
        offset_y += player.y_vel

    return offset_y

def restart_position(player):
    """
    Restart the player's position.
    """
    player.rect.x = 200
    player.rect.y = 500

def handle_events(*args):
    """
    Handle user input events.
    """
    player, game_active, offset_x, offset_y, objects, collectable, enemies, collected_count, hit_cooldown, robotnic_lives = args

    for event in pygame.event.get():
        if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            pygame.quit()
            sys.exit()

        if not game_active and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            game_active = True
        elif game_active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and player.jump_count < 2:
                player.jump()
            elif event.key == pygame.K_r:
                restart_position(player)
                offset_x = 0
                offset_y = 0

    for enemy in enemies:
        if player.rect.colliderect(enemy.rect) and hit_cooldown <= 0:
            hit_sound = pygame.mixer.Sound("game/assets/sound/hitz.wav")
            hit_sound.play()
            enemy.reset_position(enemy.rect.x, enemy.rect.y - 200)
            hit_cooldown = 5 * FPS
            robotnic_lives -= 1
            if robotnic_lives == 0:
                game_win(screen, collected_count)
                break

    if hit_cooldown > 0:
        hit_cooldown -= 1

    return game_active, offset_x, offset_y, objects, collectable, enemies

def check_flag_collision(*args):
    """
    Check collision with the flag and advance to the next level if necessary.
    """
    player, objects, level_number, collected_count,collectable,flag_1,enemies,offset_x,offset_y,flying_enemy = args
    for flag in objects:
        if isinstance(flag, flag_1) and flag.check_collision(player) or player.rect.x > 9400:
            score = collected_count * 100
            pause_screen(screen, score)
            level_number += 1
            if level_number == 0:
                objects, collectable = load_level_objects(level_1, BLOCK_SIZE)
            elif level_number == 2:
                objects, collectable = load_level_objects(level_2, BLOCK_SIZE)
            elif level_number == 3:
                objects, collectable = load_level_objects(level_3, BLOCK_SIZE)
                enemies.append(flying_enemy)
            restart_position(player)
            offset_x = 0
            offset_y = 0
            return objects,collectable, level_number,offset_x,offset_y

    for ring in collectable:
        if player.rect.colliderect(ring.rect) and not ring.collected:
            ring.collected = True
            ring.image = pygame.image.load("game/assets/img/traps/ring/empty32.png").convert_alpha()
            pick = pygame.mixer.Sound("game/assets/sound/ring.wav")
            pick.play()
            collected_count += 1
    return objects,collectable, level_number, offset_x,offset_y

def check_ring_collsion(player,collectable,collected_count):
    """
    Check collision with the rings and update the collected count.
    """
    for ring in collectable:
        if player.rect.colliderect(ring.rect) and not ring.collected:
            ring.collected = True
            ring.image = pygame.image.load("game/assets/img/traps/ring/empty32.png").convert_alpha()
            pick = pygame.mixer.Sound("game/assets/sound/ring.wav")
            pick.play()
            collected_count += 1
    return collected_count
