import pytest
from unittest.mock import patch, MagicMock
from darca_space_git.space_git import SpaceGitManager
from darca_space_git.exceptions import SpaceGitException
from darca_git.git import GitException


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_init_repo_success(mock_git, mock_file, mock_space):
    mock_git().init.return_value = None
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake/path"
    mgr = SpaceGitManager()
    assert mgr.init_repo("space") is True


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_clone_repo_failure(mock_git, mock_file, mock_space):
    mock_git().clone.side_effect = GitException("fail", "CLONE_FAILED")
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake/path"
    mgr = SpaceGitManager()
    with pytest.raises(SpaceGitException):
        mgr.clone_repo("space", "https://url")


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_commit_file_create_and_commit(mock_git, mock_file, mock_space):
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake"
    mock_file().file_exists.return_value = False
    mgr = SpaceGitManager()
    assert mgr.commit_file("space", "README.md", "msg", content="# Hello") is True


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_commit_file_missing_without_content(mock_git, mock_file, mock_space):
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake"
    mock_file().file_exists.return_value = False
    mgr = SpaceGitManager()
    with pytest.raises(SpaceGitException):
        mgr.commit_file("space", "README.md", "msg")


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_checkout_path_str_mode(mock_git, mock_file, mock_space):
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake"
    mock_file().file_exists.return_value = True
    mgr = SpaceGitManager()
    assert mgr.checkout_path("space", "README.md") is True


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_checkout_path_missing_file(mock_git, mock_file, mock_space):
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake"
    mock_file().file_exists.return_value = False
    mgr = SpaceGitManager()
    with pytest.raises(SpaceGitException):
        mgr.checkout_path("space", "README.md")


@patch("darca_space_git.space_git.SpaceManager")
@patch("darca_space_git.space_git.SpaceFileManager")
@patch("darca_space_git.space_git.Git")
def test_checkout_branch_dry_run(mock_git, mock_file, mock_space, caplog):
    mock_space().space_exists.return_value = True
    mock_space()._get_space_path.return_value = "/fake"
    mgr = SpaceGitManager()
    assert mgr.checkout_branch("space", "dev", create=True, dry_run=True) is True
    assert "Would checkout branch 'dev'" in caplog.text
