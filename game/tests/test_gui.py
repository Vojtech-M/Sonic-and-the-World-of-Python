import pygame
import sys
from game import gui
import pytest
from game.config import Pixelated_font, LIVES
from game.gui import draw_text, display_time


from pylint.lint import Run
from pylint.reporters import CollectingReporter
import ast
import inspect

@pytest.fixture(scope="session")
def linter():
    """ Test codestyle for sonic.py file. """
    src_file = 'game/gui.py'
    rep = CollectingReporter()
    # disabled warnings:
    # 0301 line too long
    # 0103 variables name (does not like shorter than 2 chars)
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

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))


def test_draw_text():
    # Clear the screen with white color
    screen.fill((255, 255, 255))
    
    # Call the function to draw text
    gui.draw_text(screen, "Hello, World!", Pixelated_font, (255, 255, 0), (100, 100))
    
    # Get colors around the specified position (100, 100) in a small radius
    radius = 5  
    colors_around_position = [
        screen.get_at((x, y)) for x in range(100 - radius, 100 + radius + 1)
        for y in range(100 - radius, 100 + radius + 1)
    ]
    
    # Check if any of the sampled colors match the expected color (yellow)
    expected_color = (255, 255, 0, 255)
    assert any(color == expected_color for color in colors_around_position)
