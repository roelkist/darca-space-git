import pytest
from darca_git.git import GitException

from darca_space_git.exceptions import SpaceGitException


def test_init_repo_success(space_git):
    assert space_git.init_repo("test-space") is True


def test_init_repo_failure(space_git):
    space_git.git.init.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.init_repo("test-space")
    assert exc.value.error_code == "INIT_FAILED"


def test_clone_repo_success(space_git):
    assert (
        space_git.clone_repo("test-space", "https://example.com/repo.git")
        is True
    )


def test_clone_repo_failure(space_git):
    space_git.git.clone.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.clone_repo("test-space", "url")
    assert exc.value.error_code == "CLONE_FAILED"


def test_get_status_success(space_git):
    space_git.git.status.return_value = "M modified"
    assert space_git.get_status("test-space") == "M modified"


def test_get_status_failure(space_git):
    space_git.git.status.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.get_status("test-space")
    assert exc.value.error_code == "STATUS_FAILED"


def test_commit_all_success(space_git):
    assert space_git.commit_all("test-space", "commit message") is True


def test_commit_all_failure(space_git):
    space_git.git.commit.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.commit_all("test-space", "commit message")
    assert exc.value.error_code == "COMMIT_ALL_FAILED"


def test_commit_file_create_and_commit(space_git):
    space_git.file_manager.file_exists.return_value = False
    assert (
        space_git.commit_file(
            "test-space", "newfile.txt", "init commit", content="data"
        )
        is True
    )


def test_commit_file_already_exists(space_git):
    space_git.file_manager.file_exists.return_value = True
    assert (
        space_git.commit_file("test-space", "existing.txt", "update commit")
        is True
    )


def test_commit_file_failure(space_git):
    space_git.file_manager.file_exists.return_value = True
    space_git.git.commit.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.commit_file("test-space", "file.txt", "failing commit")
    assert exc.value.error_code == "COMMIT_FILE_FAILED"


def test_commit_file_missing_and_no_content(space_git):
    space_git.file_manager.file_exists.return_value = False
    with pytest.raises(SpaceGitException) as exc:
        space_git.commit_file("test-space", "missing.txt", "msg", content=None)
    assert exc.value.error_code == "FILE_MISSING"


def test_pull_repo_success(space_git):
    assert space_git.pull_repo("test-space") is True


def test_pull_repo_failure(space_git):
    space_git.git.pull.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.pull_repo("test-space")
    assert exc.value.error_code == "PULL_FAILED"


def test_push_repo_success(space_git):
    assert space_git.push_repo("test-space", remote_url="origin") is True


def test_push_repo_failure(space_git):
    space_git.git.push.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.push_repo("test-space", remote_url="origin")
    assert exc.value.error_code == "PUSH_FAILED"


def test_get_repo_path_space_not_found(space_git):
    space_git.space_manager.space_exists.return_value = False
    with pytest.raises(SpaceGitException) as exc:
        space_git.init_repo("unknown-space")
    assert exc.value.error_code == "SPACE_NOT_FOUND"


def test_checkout_branch_success(space_git):
    assert space_git.checkout_branch("test-space", "feature-branch") is True


def test_checkout_branch_dry_run(space_git):
    assert space_git.checkout_branch("test-space", "dev", dry_run=True) is True


def test_checkout_branch_failure(space_git):
    space_git.git.checkout_branch.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.checkout_branch("test-space", "fail-branch")
    assert exc.value.error_code == "CHECKOUT_BRANCH_FAILED"


def test_checkout_path_success(space_git):
    space_git.file_manager.file_exists.return_value = True
    assert space_git.checkout_path("test-space", ["file.txt"]) is True


def test_checkout_path_dry_run(space_git):
    space_git.file_manager.file_exists.return_value = True
    assert (
        space_git.checkout_path("test-space", "file.txt", dry_run=True) is True
    )


def test_checkout_path_missing_file(space_git):
    space_git.file_manager.file_exists.return_value = False
    with pytest.raises(SpaceGitException) as exc:
        space_git.checkout_path("test-space", "missing.txt")
    assert exc.value.error_code == "CHECKOUT_PATH_NOT_FOUND"


def test_checkout_path_failure(space_git):
    space_git.file_manager.file_exists.return_value = True
    space_git.git.checkout_path.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.checkout_path("test-space", ["file.txt"])
    assert exc.value.error_code == "CHECKOUT_FILE_FAILED"


def test_checkout_path_from_branch_success(space_git):
    assert (
        space_git.checkout_path_from_branch(
            "test-space", "file.txt", branch="main"
        )
        is True
    )


def test_checkout_path_from_branch_dry_run(space_git):
    assert (
        space_git.checkout_path_from_branch(
            "test-space", ["file.txt"], "main", dry_run=True
        )
        is True
    )


def test_checkout_path_from_branch_failure(space_git):
    space_git.git.checkout_path_from_branch.side_effect = GitException("fail")
    with pytest.raises(SpaceGitException) as exc:
        space_git.checkout_path_from_branch("test-space", ["file.txt"], "dev")
    assert exc.value.error_code == "CHECKOUT_FILE_FROM_BRANCH_FAILED"
