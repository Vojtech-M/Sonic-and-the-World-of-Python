""""
This module contains the main function that controls the flow of the game. It initializes the game state, handles user input,
"""
import random
import pygame

from game.utils import load_level_objects, flag, FlyingEnemy
from game.player import handle_move, Player, update_offset_y, update_offset_x, handle_events, check_flag_collision, check_ring_collsion
from game.gui import game_over, draw, start_menu,play_level_music,play_intro
from game.enemy import restart_enemy_position,handle_enemy_collision,check_enemies,bullet_collision
from game.config import FPS, screen, WIDTH, HEIGHT, SCROLL_AREA_WIDTH, SCROLL_AREA_HEIGHT, max_fall_distance, BLOCK_SIZE, level_1,clock

pygame.init()
play_intro()

def main():
    """
    The main function controls the flow of the game. It initializes the game state, handles user input, 
    updates the game objects, and renders the game on the screen.
    """

    # inicializaion of game variables
    game_active = False
    robotnic_lives = 6
    offset_x = 0
    offset_y = 0
    hit_cooldown = 0
    reset_cooldown = 0
    collected_count = 0
    level_number = 1
    player = Player(200, 500, 2, 2)
    objects, collectable = load_level_objects(level_1, BLOCK_SIZE)
    FlyingEnemy.bullet_cooldown_time = random.randint(100, 200)
    flying_enemy = FlyingEnemy(1500, 300, 50, 50, 1500, 2500, 4)
    enemies = []
    green_hill_music_played = False
    boss_music_played = False

    # main game loop
    while True:
        clock.tick(FPS)
        game_active,offset_x, offset_y, objects, collectable, enemies = handle_events(player, game_active, offset_x, offset_y, objects, collectable, enemies, collected_count, hit_cooldown, robotnic_lives)

        if game_active:
            # audio
            boss_music_played, green_hill_music_played = play_level_music(level_number, boss_music_played, green_hill_music_played)

            # player movment
            player.loop(FPS)
            handle_move(player, objects)
            offset_x = update_offset_x(player, offset_x, SCROLL_AREA_WIDTH, WIDTH)
            offset_y = update_offset_y(player, offset_y, SCROLL_AREA_HEIGHT, HEIGHT)

            # handle player fall out
            offset_x, offset_y = player.fall(max_fall_distance, offset_x, offset_y)

            draw(screen, player, objects, enemies, collectable, offset_x, offset_y, collected_count)
            bullet_collision(flying_enemy, player)
            check_enemies(objects)
            reset_cooldown = restart_enemy_position(reset_cooldown,flying_enemy)
            hit_cooldown, reset_cooldown, robotnic_lives = handle_enemy_collision(player, enemies, hit_cooldown, reset_cooldown, robotnic_lives,collected_count)
            hit_cooldown = max(0, hit_cooldown - 1)
            collected_count = check_ring_collsion(player, collectable, collected_count)
            objects,collectable, level_number,offset_x,offset_y = check_flag_collision(player, objects, level_number, collected_count,collectable,flag, enemies,offset_x,offset_y,flying_enemy)

            game_over(player,screen)
        else:
            # intro after start
            start_menu(screen, 640)
        pygame.display.update()
if __name__ == "__main__":
    main()
