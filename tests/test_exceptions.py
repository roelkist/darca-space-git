from darca_space_git.exceptions import SpaceGitException


def test_space_git_exception_full_coverage():
    cause = ValueError("original error")
    metadata = {"space": "example-space", "file": "README.md"}

    exc = SpaceGitException(
        message="Something went wrong in space-git",
        error_code="SPACE_GIT_FAIL",
        metadata=metadata,
        cause=cause,
    )

    assert isinstance(exc, SpaceGitException)
    assert exc.message == "Something went wrong in space-git"
    assert exc.error_code == "SPACE_GIT_FAIL"
    assert exc.metadata == metadata
    assert "original error" in str(exc)
    assert "SPACE_GIT_FAIL" in repr(exc)
