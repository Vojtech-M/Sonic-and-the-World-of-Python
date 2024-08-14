"""
This module contains the functions that are responsible for the enemies in the game.
"""
import random
import pygame
from game.config import FPS, screen
from game.utils import FlyingEnemy
from game.gui import game_win

def bullet_collision(flying_enemy, player):
    """
    Check for collision between the player and the flying enemy's bullets.

    Args:
        flying_enemy: The flying enemy object.
        player: The player object.
    """
    for bullet in flying_enemy.bullets:
        if player.rect.colliderect(bullet.rect):
            player.make_hit()
            hit_sound = pygame.mixer.Sound("game/assets/sound/hit.wav")
            hit_sound.play()
            bullet.lifespan = 0
            break

def restart_enemy_position(reset_cooldown, flying_enemy):
    """
    Reset the enemy's position and image after a certain amount of time.
    """
    if reset_cooldown > 0:
        reset_cooldown -= 1
        if reset_cooldown == 0:
            flying_enemy.reset_position(flying_enemy.rect.x, flying_enemy.rect.y + 200)
            FlyingEnemy.bullet_cooldown_time = random.randint(100, 200)
            flying_enemy.change_image("game/assets/img/enemy/robotnic/dr_robotnic.png")
    return reset_cooldown

def handle_enemy_collision(*args):
    """
    Check for collision between the player and the enemies.
    """
    player, enemies, hit_cooldown, reset_cooldown, robotnic_lives, collected_count = args
    for enemy in enemies:
        enemy.update(player)
        if player.rect.colliderect(enemy.rect) and hit_cooldown <= 0:
            hit_sound = pygame.mixer.Sound("game/assets/sound/hit.wav")
            hit_sound.play()
            enemy.reset_position(enemy.rect.x, enemy.rect.y - 200)
            FlyingEnemy.bullet_cooldown_time = 20
            hit_cooldown = 5 * FPS
            reset_cooldown = 5 * FPS
            robotnic_lives -= 1
            enemy.change_image("game/assets/img/enemy/robotnic/dr_robotnic_angry.png")
            if robotnic_lives == 0:
                game_win(screen, collected_count)
                break
    return hit_cooldown, reset_cooldown, robotnic_lives

def check_enemies(objects):
    """
    Check if the enemies are still on the screen.
    """
    for crub in objects:
        crub.update(FPS)
    for bat in objects:
        bat.update(FPS)
