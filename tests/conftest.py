import pytest
import os
import sys

# Add the path of the directory one level above to the list of module searching paths
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from sort import *

# Preparation of data for tests
@pytest.fixture(scope="module")
def app():
    app = Application()
    jumble_a_collection()
    yield app