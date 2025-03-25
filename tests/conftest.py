import pytest
from unittest.mock import MagicMock, patch
from darca_space_git.space_git import SpaceGitManager

@pytest.fixture
def space_git():
    return SpaceGitManager()
