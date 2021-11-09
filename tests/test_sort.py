import pytest
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sort import *

# Whether the processing reaches the sorting program
def test_process(mocker, app):
    quick_sort = mocker.patch("sort.quick_sort")
    set_animation = mocker.patch("sort.Canvas.set_animation")

    app.process()

    quick_sort.assert_called_once_with(0, len(COL)-1)
    set_animation.assert_called_once_with()

# Whether the sorting function expectedly outputs after executed
def test_sort(app):
    assert COL != sorted(COL)
    assert not RECORD

    app.process()

    assert COL == sorted(COL)
    assert RECORD