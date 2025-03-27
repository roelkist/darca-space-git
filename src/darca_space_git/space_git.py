from typing import List, Optional, Union

from darca_git.git import Git, GitException
from darca_log_facility.logger import DarcaLogger
from darca_space_manager.space_file_manager import SpaceFileManager
from darca_space_manager.space_manager import SpaceManager

from .exceptions import SpaceGitException

logger = DarcaLogger(name="space_git").get_logger()


class SpaceGitManager:
    """
    Manages Git operations within darca-space-managed logical spaces.

    This manager ensures that all Git interactions occur within paths allocated
    by the `SpaceManager`. All operations are scoped to these managed spaces
    and avoid any direct user interaction with the file system.
    """

    def __init__(self) -> None:
        self.git = Git()
        self.space_manager = SpaceManager()
        self.file_manager = SpaceFileManager()

    def _get_repo_path(self, space_name: str) -> str:
        """
        Resolve the absolute path of a given logical space.

        Raises:
            SpaceGitException: If the space does not exist.

        Returns:
            str: Filesystem path to the Git repository.
        """
        if not self.space_manager.space_exists(space_name):
            raise SpaceGitException(
                message=f"Space '{space_name}' does not exist.",
                error_code="SPACE_NOT_FOUND",
                metadata={"space": space_name},
            )
        return self.space_manager._get_space_path(space_name)

    def init_repo(self, space_name: str) -> bool:
        """
        Initialize a new Git repository in the given space.

        Returns:
            bool: True if successful.

        Raises:
            SpaceGitException: If initialization fails.
        """
        path = self._get_repo_path(space_name)
        try:
            self.git.init(path)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to initialize git repository.",
                error_code="INIT_FAILED",
                metadata={"space": space_name},
                cause=e,
            )

    def clone_repo(self, space_name: str, repo_url: str) -> bool:
        """
        Clone a Git repository into the given space.

        Args:
            repo_url (str): URL of the remote repository.

        Returns:
            bool: True if successful.

        Raises:
            SpaceGitException: If cloning fails.
        """
        path = self._get_repo_path(space_name)
        try:
            self.git.clone(repo_url, cwd=path)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to clone repository.",
                error_code="CLONE_FAILED",
                metadata={"space": space_name, "url": repo_url},
                cause=e,
            )

    def get_status(self, space_name: str, porcelain: bool = True) -> str:
        """
        Retrieve the Git status of the repository.

        Args:
            porcelain (bool): Whether to return porcelain output.

        Returns:
            str: Output of `git status`.

        Raises:
            SpaceGitException: If status command fails.
        """
        path = self._get_repo_path(space_name)
        try:
            return self.git.status(path, porcelain=porcelain)
        except GitException as e:
            raise SpaceGitException(
                message="Failed to get git status.",
                error_code="STATUS_FAILED",
                metadata={"space": space_name, "porcelain": porcelain},
                cause=e,
            )

    def commit_all(self, space_name: str, message: str) -> bool:
        """
        Stage and commit all changes in the repository.

        Args:
            message (str): Commit message.

        Returns:
            bool: True if successful.

        Raises:
            SpaceGitException: If committing fails.
        """
        path = self._get_repo_path(space_name)
        try:
            self.git.add(".", cwd=path)
            self.git.commit(message, cwd=path)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to commit all changes.",
                error_code="COMMIT_ALL_FAILED",
                metadata={"space": space_name, "message": message},
                cause=e,
            )

    def commit_file(
        self,
        space_name: str,
        relative_path: str,
        message: str,
        content: Optional[Union[str, dict]] = None,
    ) -> bool:
        """
        Commit a specific file. Creates the file if it doesn't exist and
        content is provided.

        Args:
            relative_path (str): Path to the file relative to the space root.
            message (str): Commit message.
            content (Optional[str | dict]): Optional file content to create if
            missing.

        Returns:
            bool: True if successful.

        Raises:
            SpaceGitException: If file is missing with no content, or commit
            fails.
        """
        path = self._get_repo_path(space_name)
        try:
            if not self.file_manager.file_exists(space_name, relative_path):
                if content is None:
                    raise SpaceGitException(
                        message="File does not exist and no content provided.",
                        error_code="FILE_MISSING",
                        metadata={"space": space_name, "file": relative_path},
                    )
                self.file_manager.set_file(space_name, relative_path, content)
                logger.debug(
                    f"Created file '{relative_path}' in space '{space_name}'"
                )

            self.git.add(relative_path, cwd=path)
            self.git.commit(message, cwd=path)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to commit file.",
                error_code="COMMIT_FILE_FAILED",
                metadata={"space": space_name, "file": relative_path},
                cause=e,
            )

    def pull_repo(self, space_name: str) -> bool:
        """
        Pull the latest changes from the remote repository.

        Returns:
            bool: True if successful.

        Raises:
            SpaceGitException: If pull operation fails.
        """
        path = self._get_repo_path(space_name)
        try:
            self.git.pull(path)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to pull repository.",
                error_code="PULL_FAILED",
                metadata={"space": space_name},
                cause=e,
            )

    def push_repo(
        self, space_name: str, remote_url: Optional[str] = None
    ) -> bool:
        """
        Push local changes to the remote repository.

        Args:
            remote_url (Optional[str]): Optional remote URL to push to.

        Returns:
            bool: True if successful.

        Raises:
            SpaceGitException: If push operation fails.
        """
        path = self._get_repo_path(space_name)
        try:
            self.git.push(cwd=path, remote_url=remote_url)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to push repository.",
                error_code="PUSH_FAILED",
                metadata={"space": space_name, "remote_url": remote_url},
                cause=e,
            )

    def checkout_branch(
        self,
        space_name: str,
        branch: str,
        create: bool = False,
        dry_run: bool = False,
    ) -> bool:
        """
        Checkout an existing or new branch.

        Args:
            branch (str): Branch name.
            create (bool): Whether to create the branch.
            dry_run (bool): If True, simulate without making changes.

        Returns:
            bool: True if successful or simulated.

        Raises:
            SpaceGitException: If checkout fails.
        """
        path = self._get_repo_path(space_name)
        if dry_run:
            logger.info(
                f"[DRY-RUN] Would checkout branch '{branch}' "
                f"(create={create}) in space '{space_name}'"
            )
            return True

        try:
            self.git.checkout_branch(cwd=path, branch=branch, create=create)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to checkout branch.",
                error_code="CHECKOUT_BRANCH_FAILED",
                metadata={
                    "space": space_name,
                    "branch": branch,
                    "create": create,
                },
                cause=e,
            )

    def checkout_path(
        self,
        space_name: str,
        paths: Union[str, List[str]],
        dry_run: bool = False,
    ) -> bool:
        """
        Revert file(s) in the working directory to the last committed state.

        Args:
            paths (str | List[str]): File path(s) relative to space root.
            dry_run (bool): If True, simulate the operation.

        Returns:
            bool: True if successful or simulated.

        Raises:
            SpaceGitException: If file is missing or operation fails.
        """
        if isinstance(paths, str):
            paths = [paths]

        missing = [
            p
            for p in paths
            if not self.file_manager.file_exists(space_name, p)
        ]
        if missing:
            raise SpaceGitException(
                message="Some files do not exist in the working directory.",
                error_code="CHECKOUT_PATH_NOT_FOUND",
                metadata={"space": space_name, "missing_files": missing},
            )

        path = self._get_repo_path(space_name)
        if dry_run:
            logger.info(
                f"[DRY-RUN] Would revert: {', '.join(paths)} "
                f"in space '{space_name}'"
            )
            return True

        try:
            self.git.checkout_path(cwd=path, paths=paths)
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to revert file(s).",
                error_code="CHECKOUT_FILE_FAILED",
                metadata={"space": space_name, "files": paths},
                cause=e,
            )

    def checkout_path_from_branch(
        self,
        space_name: str,
        paths: Union[str, List[str]],
        branch: str,
        dry_run: bool = False,
    ) -> bool:
        """
        Restore file(s) from a specific branch into the working directory.

        Args:
            paths (str | List[str]): Path(s) to restore.
            branch (str): Source branch.
            dry_run (bool): If True, simulate the operation.

        Returns:
            bool: True if successful or simulated.

        Raises:
            SpaceGitException: If restore fails.
        """
        if isinstance(paths, str):
            paths = [paths]

        path = self._get_repo_path(space_name)
        if dry_run:
            logger.info(
                f"[DRY-RUN] Would restore: {', '.join(paths)} from branch "
                f"'{branch}' in space '{space_name}'"
            )
            return True

        try:
            self.git.checkout_path_from_branch(
                cwd=path, branch=branch, paths=paths
            )
            return True
        except GitException as e:
            raise SpaceGitException(
                message="Failed to restore file(s) from branch.",
                error_code="CHECKOUT_FILE_FROM_BRANCH_FAILED",
                metadata={
                    "space": space_name,
                    "files": paths,
                    "branch": branch,
                },
                cause=e,
            )
