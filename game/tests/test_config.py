from game.config import *
import pytest
from pylint.lint import Run
from pylint.reporters import CollectingReporter
import ast
import inspect

@pytest.fixture(scope="session")
def linter():
    """ Test codestyle for sonic.py file. """
    src_file = 'game/config.py'
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
