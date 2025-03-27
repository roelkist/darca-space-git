from unittest.mock import patch

import pytest

from darca_space_git.space_git import SpaceGitManager


@pytest.fixture
def space_git():
    with patch(
        "darca_space_git.space_git.SpaceManager"
    ) as MockSpaceManager, patch(
        "darca_space_git.space_git.SpaceFileManager"
    ), patch(
        "darca_space_git.space_git.Git"
    ) as MockGit:

        mock_space_manager = MockSpaceManager.return_value
        MockGit.return_value

        mock_space_manager.space_exists.return_value = True
        mock_space_manager._get_space_path.return_value = "/fake/path"

        yield SpaceGitManager()
