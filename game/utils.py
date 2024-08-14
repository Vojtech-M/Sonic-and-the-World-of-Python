"""
This module contains logic functions and classes for the game.
"""
import os
import pygame
from game.config import BAT_IMAGE_PATHS, CRUB_IMAGE_PATHS

def flip(sprites):
    """
    Flips the given sprites horizontally.
    Args:
        sprites (list): A list of pygame.Surface objects representing the sprites to be flipped.
    Returns:
        list: A new list of pygame.Surface objects with the sprites flipped horizontally.
    """
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    """
    Loads sprite sheets from the specified directory and returns a dictionary of sprites.
    """
    path = os.path.join("game", "assets", dir1, dir2)
    images = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    all_sprites = {}
    for image in images:
        sprite_sheet = pygame.image.load(os.path.join(path, image)).convert_alpha()
        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))
        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = [pygame.transform.flip(sprite, True, False) for sprite in sprites]
        else:
            all_sprites[image.replace(".png", "")] = sprites
    return all_sprites

def get_block(size, start_x, start_y):
    """
    Extract block from given sprite sheet.
    args:
        size (int): Size of the block.
        start_x (int): x-coordinate of the block.
        start_y (int): y-coordinate of the block.
    """
    # load the sprite sheet
    image = pygame.image.load("game/assets/img/terrain/teren.png").convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(start_x, start_y, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

class Object(pygame.sprite.Sprite):
    """
    Generic object class for all objects in the game.
    """
    def __init__(self, x, y, width, height, name=None):
        """
        Inicialization of generic object.
        """
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x,offset_y):
        """
        Draw the object on the screen.
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class Spike(Object):
    """
    Block with collision.
    """
    def __init__(self, x, y, width, height):
        """
        Inicialization of spike object.
        """
        super().__init__(x, y, width, height, "Spike")
        self.image = pygame.image.load("game/assets/img/traps/Spike/Spikes.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (96, 96)) # size
        self.mask = pygame.mask.from_surface(self.image)

class AnimatedObject(Object):
    """
    Object with animation.
    """
    def __init__(self, x, y, width, height, image_paths, image_size, frame_delay, name=None):
        """
        Inicialization of animated object.
        """
        super().__init__(x, y, width, height, name)
        self.images = [pygame.transform.scale(pygame.image.load(path).convert_alpha(), image_size) for path in image_paths]
        self.image_index = 0
        self.image = self.images[self.image_index]
        self.frame_delay = frame_delay  

    def update(self, dt):
        """
        Update the object's animation.
        """
        self.frame_delay -= dt
        if self.frame_delay <= 0:
            self.frame_delay = self.FRAME_DELAY
            self.image_index = (self.image_index + 1) % len(self.images)
            self.image = self.images[self.image_index]

class Crub(AnimatedObject):
    """
    Crub enemy object.
    """
    IMAGE_PATHS = CRUB_IMAGE_PATHS
    IMAGE_SIZE = (96, 96)
    FRAME_DELAY = 800  # Delay between frame changes
    def __init__(self, x, y, width, height):
        """
        Inicialization of crub enemy.
        """
        super().__init__(x, y, width, height, self.IMAGE_PATHS, self.IMAGE_SIZE, self.FRAME_DELAY, "Crub")

class Bat(AnimatedObject):
    """
    Inicialization of bat enemy.
    """
    IMAGE_PATHS = BAT_IMAGE_PATHS
    IMAGE_SIZE = (160, 160)
    FRAME_DELAY = 500  # Delay between frame changes

    def __init__(self, x, y, width, height):
        """
        Initialize a bat enemy object.
        """
        super().__init__(x, y, width, height, self.IMAGE_PATHS, self.IMAGE_SIZE, self.FRAME_DELAY, "Bat")

class Block(Object):
    """
    Block object to build the levels.
    """
    def __init__(self, x, y, size,start_x,start_y):
        """
        Initialize a block object.
        """
        super().__init__(x, y, size, start_x,start_y)
        block = get_block(size,start_x,start_y)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class collectable(Object):
    """
    Collectable object to collect in the game.
    """
    def __init__(self, x, y, width, height, name=None):
        """
        Initialize a collectable object.
        """
        super().__init__(x, y, width, height, name)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.collected = False

class Ring(collectable):
    """
    The ring collectable object.
    """
    def __init__(self, x, y, width, height):
        """
        Initialize a ring collectable object.
        """
        super().__init__(x, y, width, height)
        self.image = pygame.image.load("game/assets/img/traps/ring/ring50.png").convert_alpha()

def load_level_objects(level_data, BLOCK_SIZE):
    """
    Load all objects from the level
    Args:
        level_data (np.array): A NumPy array representing the level layout.
        BLOCK_SIZE (int): The size of each block in the level.
    Returns:
        list: A list of objects in the level.
    """
    objects = []
    collectables = []
    for y in range(level_data.shape[0]):
        for x in range(level_data.shape[1]):
            if level_data[y, x] == 1: # Basic block
                objects.append(Block(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, 96, 64))
            elif level_data[y, x] == 2: # Grass block
                objects.append(Block(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, 96, 0))
            elif level_data[y, x] == 3: # Spike
                objects.append(Spike(x * BLOCK_SIZE, y * BLOCK_SIZE, 16, 32))
            elif level_data[y, x] == 4: # Ring
                collectables.append(Ring(x * BLOCK_SIZE, y * BLOCK_SIZE, 32, 32))
            elif level_data[y, x] == 5: # Basic block with shadow
                objects.append(Block(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, 193, 65))
            elif level_data[y, x] == 6: # Basic block right corner
                objects.append(Block(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, 96, 128))
            elif level_data[y, x] == 7: # End level flag
                objects.append(flag(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, 150))
            elif level_data[y, x] == 8:  # Crub enemy
                objects.append(Crub(x * BLOCK_SIZE, y * BLOCK_SIZE, 16, 32))
            elif level_data[y, x] == 9:  # Bat enemy
                objects.append(Bat(x * BLOCK_SIZE, y * BLOCK_SIZE, 16, 32))
    return objects, collectables

class flag(Object):
    """
    End level object to finish the level.
    """
    def __init__(self, x, y, width, height):
        """
        Initialize the end-level object.       
        
        """
        super().__init__(x, y, width, height)
        self.image = pygame.image.load("game/assets/img/flag/end_flag.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (96, 96))

    def check_collision(self, player):
        """
        Check collision between the player and the end-level object.
        If collision occurs, change the level.
        """
        return self.rect.colliderect(player.rect)

class Bullets(pygame.sprite.Sprite):
    """
    Inicialization of bullets.
    """
    def __init__(self, x, y, image_path, speed):
        """
        Initialize a bullet object.
        """
        super().__init__()
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x  # Set the initial coordinates
        self.rect.y = y
        self.speed = speed
        self.lifespan = 120  # Lifespan of the bullet in frames

    def update_position(self, player):
        """
        Update the bullet's position based on the player's position.
        """
        # Calculate the distance between the bullet and the player
        dx = player.rect.x - self.rect.x + 50
        dy = player.rect.y - self.rect.y + 50

        # Move the bullet towards the player with a reduced speed
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def draw(self, win, offset_x, offset_y):
        """
        Draw the bullet on the screen.
        """
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))

class FlyingEnemy(pygame.sprite.Sprite):
    """ 
    Final boss enemy.
    """
    def __init__(self,*args):
        """
        Inicialization of flying enemy.
        """
        x, y, width, height, start_x, end_x, speed = args
        super().__init__()
        self.rect = pygame.Rect(x, y, 100, 100) 
        self.start_x = start_x # Positions
        self.end_x = end_x 
        self.speed = speed 
        self.direction = 1  # 1 for moving right, -1 for moving left
        self.original_image = pygame.image.load("game/assets/img/enemy/robotnic/dr_robotnic.png").convert_alpha()
        self.image = pygame.transform.scale(self.original_image, (width * 4, height * 4))  # Scale up the image
        self.mask = pygame.mask.from_surface(self.image, 127)
        self.bullets = []  # List to store bullet instances
        self.bullet_cooldown = 0  # Counter to track cooldown

    def reset_position(self, x, y):
        """
        Reset the enemy's position.
        """
        # Reset enemy position
        self.rect.x = x
        self.rect.y = y

    def draw(self, window, offset_x, offset_y):
        """
        Draw the enemy on the screen.
        """
        # Draw the enemy on the screen
        window.blit(self.image, (self.rect.x - offset_x, self.rect.y - offset_y))
        # Draw bullets on the screen
        for bullet in self.bullets:
            bullet.draw(window, offset_x, offset_y)

    def shoot_bullet(self):
        """
        Shoot a bullet towards the player.
        """
        # Create a new bullet instance originating from the enemy's position
        bullet = Bullets(self.rect.x, self.rect.y, "game/assets/img/enemy/robotnic/bullet.png", 0.02)
        shoot_sound = pygame.mixer.Sound("game/assets/sound/laser_shot.wav")
        shoot_sound.play()
        self.bullets.append(bullet)

    def update(self,player):
        """
        Update the enemy's position and shoot bullets.
        """
        # Update enemy position based on direction and speed
        self.rect.x += self.direction * self.speed

        # Check if enemy reached the end position, then change direction
        if self.rect.x <= self.start_x:
            self.direction = 1
        elif self.rect.x >= self.end_x:
            self.direction = -1
        # Update bullets' positions
        for bullet in self.bullets:
            bullet.update_position(player)
        # Remove bullets that exceed their lifespan
        self.bullets = [bullet for bullet in self.bullets if bullet.lifespan > 0]
        for bullet in self.bullets:
            bullet.lifespan -= 1
        self.rect.x += self.direction * self.speed
        if self.bullet_cooldown > 0:
            self.bullet_cooldown -= 1
        # Check if the player is within shooting range
        # could be used for more logic
        distance_to_player = abs(player.rect.x - self.rect.x)
        if distance_to_player < 5000 and self.bullet_cooldown == 0:
            # Shoot a bullet towards the player
            self.shoot_bullet()
            self.bullet_cooldown = self.bullet_cooldown_time

    def change_image(self, new_image_path):
        """
        Change the enemy's image to the specified image.
        """
        new_image = pygame.image.load(new_image_path).convert_alpha()
        original_width, original_height = self.image.get_size()
        # Scale the new image to match the original size
        new_image = pygame.transform.scale(new_image, (original_width, original_height))
        self.image = new_image
        self.mask = pygame.mask.from_surface(self.image, 127)
