import pytest
import pygame
from game.player import Player, collide, handle_vertical_collision
from game.player import check_flag_collision

from pylint.lint import Run
from pylint.reporters import CollectingReporter
import ast
import inspect

@pytest.fixture(scope="session")
def linter():
    """ Test codestyle for sonic.py file. """
    src_file = 'game/player.py'
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
    # E1101 collision with pygame
    r = Run(['--disable=C0301,C0103,E1101,R0902', '-sn', src_file], reporter=rep, exit=False)
    return r.linter

def test_codestyle_for_sonic(linter):
    """ Evaluate codestyle for sonic.py. """
    print('\nLinter output:')
    for m in linter.reporter.messages:
        print(f'{m.msg_id} ({m.symbol}) line {m.line}: {m.msg}')
    score = linter.stats.global_note
    print(f'pylint score = {score}')
    assert score >= 10  # Adjust the threshold as needed

@pytest.fixture
def player():
    return Player(0, 0, 32, 32)

@pytest.fixture
def objects():
    return []

def test_player_initialization(player):
    assert player.rect.x == 0
    assert player.rect.y == 0
    assert player.rect.width == 32
    assert player.rect.height == 32

def test_player_jump(player):
    initial_y_vel = player.y_vel
    player.jump()
    assert player.y_vel < initial_y_vel

class MockFlag:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height))
    def check_collision(self, player):
        return player.rect.colliderect(self.rect)
class MockCollectable:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.collected = False

@pytest.fixture
def flag():
    return MockFlag(100, 100, 32, 32)

@pytest.fixture
def collectable():
    return [MockCollectable(200, 200, 32, 32)]

@pytest.fixture
def objects(flag):
    return [flag]

def test_check_flag_collision_no_collision(player, objects, collectable):
    level_number = 1
    collected_count = 0
    offset_x = 0
    offset_y = 0
    flying_enemy = None
    assert check_flag_collision(player, objects, level_number, collected_count, collectable, MockFlag, [], offset_x, offset_y, flying_enemy) == (objects, collectable, level_number, offset_x, offset_y)

def test_check_flag_collision_ring_collision(player, objects, collectable):
    level_number = 1
    collected_count = 0
    offset_x = 0
    offset_y = 0
    flying_enemy = None
    assert check_flag_collision(player, objects, level_number, collected_count, collectable, MockFlag, [], offset_x, offset_y, flying_enemy) == (objects, collectable, level_number, offset_x, offset_y)
