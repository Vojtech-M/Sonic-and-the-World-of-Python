"""
This module contains the game settings and configurations.
"""
import pygame
import numpy as np

##### Game settings #####
WIDTH = 1280
HEIGHT = 720
FPS = 60
PLAYER_VEL = 8
LIVES = 6
HIT_DELAY = 800
max_fall_distance = 4000
BLOCK_SIZE = 96

pygame.font.init()
clock = pygame.time.Clock()

##### Window ############
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sonic and the world of python")
pygame_icon = pygame.image.load("game/assets/img/ui/logo.png")
pygame.display.set_icon(pygame_icon)

##### Colors #####
Pixelated_font = pygame.font.Font("game/assets/img/fonts/PublicPixel.ttf", 32)
Text_yellow = (255, 250, 1)

##### Camera #####
SCROLL_AREA_WIDTH = 500
SCROLL_AREA_HEIGHT = 120

##### Levels #####
def load_level_from_file(filename):
    """
    Load a level from a text file and return it as a NumPy array.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        level_data = np.array([[int(x) for x in line.split()] for line in f])
    return level_data

level_1 = load_level_from_file('game/assets/levels/level_1.txt')
level_2 = load_level_from_file('game/assets/levels/level_2.txt')
level_3 = load_level_from_file('game/assets/levels/level_3.txt')

##### Music #####
TITLE_SCREEN = "game/assets/sound/title_screen.mp3"
GREEN_HILL_ZONE = "game/assets/sound/green-hill-zone.mp3"
BOSS = "game/assets/sound/boss_theme.mp3"
BAT_IMAGE_PATHS = ["game/assets/img/enemy/bat/bat1.png"
                    ,"game/assets/img/enemy/bat/bat2.png"
                    ,"game/assets/img/enemy/bat/bat3.png"
                    ,"game/assets/img/enemy/bat/bat4.png"
                    ,"game/assets/img/enemy/bat/bat5.png"
                    ,"game/assets/img/enemy/bat/bat6.png"
                    ,"game/assets/img/enemy/bat/bat7.png"
                    ,"game/assets/img/enemy/bat/bat8.png"
                    ,"game/assets/img/enemy/bat/bat9.png"
                    ,"game/assets/img/enemy/bat/bat10.png"
                    ,"game/assets/img/enemy/bat/bat11.png"
                    ,"game/assets/img/enemy/bat/bat12.png"
                    ,"game/assets/img/enemy/bat/bat13.png"
                    ,"game/assets/img/enemy/bat/bat14.png"
                    ,"game/assets/img/enemy/bat/bat15.png"
                    ,"game/assets/img/enemy/bat/bat16.png"
                    ,"game/assets/img/enemy/bat/bat17.png"
                    ,"game/assets/img/enemy/bat/bat18.png"
                    ,"game/assets/img/enemy/bat/bat19.png"
                    ,"game/assets/img/enemy/bat/bat20.png"
                    ,"game/assets/img/enemy/bat/bat21.png"]
CRUB_IMAGE_PATHS = ["game/assets/img/enemy/crub/crub.png",
                    "game/assets/img/enemy/crub/crub2.png",
                    "game/assets/img/enemy/crub/crub3.png",
                    "game/assets/img/enemy/crub/crub3.png"]
