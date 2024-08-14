import pytest
import pygame
from game.enemy import restart_enemy_position, handle_enemy_collision, check_enemies
from game.config import FPS
from game.utils import FlyingEnemy
from game.gui import game_win

from game.config import *
from pylint.lint import Run
from pylint.reporters import CollectingReporter
import ast
import inspect

@pytest.fixture(scope="session")
def linter():
    """ Test codestyle for sonic.py file. """
    src_file = 'game/enemy.py'
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    # E1101 collision with pygame
    r = Run(['--disable=C0301,C0103,E1101 ', '-sn', src_file], reporter=rep, exit=False)
    return r.linter

def test_codestyle_for_sonic(linter):
    """ Evaluate codestyle for sonic.py. """
    print('\nLinter output:')
    for m in linter.reporter.messages:
        print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')
    score = linter.stats.global_note
    print(f'pylint score = {score}')
    assert score >= 10  # Adjust the threshold as needed

def test_configuration():
    assert WIDTH == 1280
    assert HEIGHT == 720
def test_restart_enemy_position():
    class MockFlyingEnemy:
        def reset_position(self, x, y):
            self.rect.x = x
            self.rect.y = y
        
        def change_image(self, image_path):
            self.image_path = image_path

    flying_enemy = MockFlyingEnemy()
    flying_enemy.rect = pygame.Rect(0, 0, 10, 10)

    reset_cooldown = restart_enemy_position(0, flying_enemy)
    assert reset_cooldown == 0

    reset_cooldown = restart_enemy_position(4, flying_enemy)
    assert reset_cooldown == 3

    reset_cooldown = restart_enemy_position(1, flying_enemy)
    assert reset_cooldown == 0
    assert flying_enemy.rect.y == 200

def test_handle_enemy_collision():
    class MockPlayer:
        def __init__(self):
            self.rect = pygame.Rect(50, 50, 10, 10)

    class MockFlyingEnemy:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, 10, 10)
        def reset_position(self, x, y):
            self.rect.x = x
            self.rect.y = y
        def update(self, player):
            pass
        def change_image(self, image_path):
            pass

    player = MockPlayer()
    enemies = [MockFlyingEnemy(50, 50), MockFlyingEnemy(200, 200)]
    hit_cooldown = 0
    reset_cooldown = 0
    Robotnic_lives = 3
    collected_count = 0

    hit_cooldown, reset_cooldown, Robotnic_lives = handle_enemy_collision(player, enemies, hit_cooldown, reset_cooldown, Robotnic_lives, collected_count)
    assert hit_cooldown == 5 * FPS
    assert reset_cooldown == 5 * FPS
    assert Robotnic_lives == 2
    assert enemies[0].rect.y == -150

    player.rect = pygame.Rect(0, 0, 10, 10)
    hit_cooldown, reset_cooldown, Robotnic_lives = handle_enemy_collision(player, enemies, hit_cooldown, reset_cooldown, Robotnic_lives, collected_count)
    assert Robotnic_lives == 2

def test_check_enemies():
    class MockEnemy:
        def __init__(self):
            self.updated = False
        def update(self, fps):
            self.updated = True

    enemies = [MockEnemy(), MockEnemy()]
    check_enemies(enemies)
    
    for enemy in enemies:
        assert enemy.updated
