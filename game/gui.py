"""
This module contains the functions that are responsible for the graphical user interface of the game
"""
import sys
import pygame
from game.config import WIDTH, HEIGHT, LIVES, Text_yellow,TITLE_SCREEN,GREEN_HILL_ZONE,BOSS

pygame.font.init()
Pixelated_font = pygame.font.Font("game/assets/img/fonts/PublicPixel.ttf", 32)

def draw_text(screen,text, font, text_color, position):
    """
    Draw text on the screen.
    Use the Publicpixel font
    args:
    screen: pygame.Surface
    text: str
    font: pygame.font.Font
    text_color: tuple
    position: tuple
    """
    img = font.render(text, True, text_color)
    screen.blit(img, (position))

def display_time(screen,minutes=0):
    """
    Display the time on the screen.
    args:
    screen: pygame.Surface
    minutes: int
    """
    current_time = pygame.time.get_ticks()
    total_seconds = current_time // 1000
    minutes, seconds = divmod(total_seconds, 60)
    time_surf = Pixelated_font.render(f'Time:{minutes:01}:{seconds:02}', False, Text_yellow)
    time_rect = time_surf.get_rect(center=(185,50))
    screen.blit(time_surf, time_rect)

def start_menu(screen, position):
    """
    Display the start menu on the screen.
    args: 
    screen: pygame.Surface
    position: int
    """
    menu_screen = pygame.image.load("game/assets/img/ui/start_screen.png")
    screen.blit(menu_screen, (0, 0))
    draw_text(screen, "Press SPACE to start", Pixelated_font, Text_yellow , (300, position))

def game_over(player,screen):
    """
    Display the game over screen.
    """
    if player.hit_count >= LIVES:
        draw_text(screen,"Game Over!", Pixelated_font, (251,250,1),(500, 300))
        pygame.display.update()
        pygame.time.delay(2000)
        sys.exit()

def play_intro():
    """
    platy the intro music
    """
    pygame.mixer.music.load(TITLE_SCREEN)
    pygame.mixer.music.play()

def draw(*args):
    """
    Draw the game objects on the screen.
    """
    window, player, objects, enemies, collectables, offset_x, offset_y, collected_count = args

    background_image = pygame.image.load("game/assets/img/ui/background.png").convert()
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Draw the background
    window.blit(background_image, (0, 0))

    # Draw objects
    for obj in objects:
        obj.draw(window, offset_x, offset_y)

    # Draw collectables
    for col in collectables:
        col.draw(window, offset_x, offset_y)

    # Draw enemies
    for enemy in enemies:
        enemy.draw(window,offset_x, offset_y)

    # Draw the player
    player.draw(window, offset_x, offset_y)

    # Draw text
    draw_text(window, f"Lives:{LIVES - player.hit_count}", Pixelated_font, Text_yellow, (50, 90))
    draw_text(window, f"Rings:{collected_count}", Pixelated_font, Text_yellow, (50, 150))

    # Display time
    display_time(window)

    # Update the display
    pygame.display.update()

def game_win(screen,collected_count):
    """
    Display the game win screen.
    """
    draw_text(screen,"You Win!", Pixelated_font, (251,250,1), (500, 300))
    score = collected_count * 100
    draw_text(screen, f"FINAL SCORE: {score}", Pixelated_font, Text_yellow , (400, 500))
    if score == 7500:
        draw_text(screen,"PERFECT ! ", Pixelated_font, Text_yellow , (400, 550))
    pygame.mixer.music.stop()
    hit_sound = pygame.mixer.Sound("game/assets/sound/ending_title.mp3")
    hit_sound.play()
    pygame.display.update()
    pygame.time.delay(6000)
    sys.exit()

def pause_screen(screen, score):
    """
    Display the pause screen.

    Args:
        screen (pygame.Surface): The screen to display the pause screen on
        score (int): The player's score
    """
    draw_text(screen, f"SCORE: {score}", Pixelated_font, Text_yellow , (500, 300))
    pygame.display.flip()
    pygame.time.delay(3000)

def play_music(music_path, loop=-1):
    """
    Function to play music with given path and loop.
    """
    pygame.mixer.music.load(music_path)
    pygame.mixer.music.play(loop)

def play_level_music(level_number, boss_music_played, green_hill_music_played):
    """
    Function to play music based on the level number and music play status.
    """
    if level_number == 3 and not boss_music_played:
        play_music(BOSS)
        boss_music_played = True
    elif not green_hill_music_played:
        play_music(GREEN_HILL_ZONE)
        green_hill_music_played = True

    return boss_music_played, green_hill_music_played
