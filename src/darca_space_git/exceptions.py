from typing import Any, Dict, Optional

from darca_exception.exception import DarcaException


class SpaceGitException(DarcaException):
    """
    Exception raised for errors originating from the darca-space-git layer.

    This exception serves as a unified abstraction for Git and space-related
    failures that occur within the context of darca-managed logical spaces.

    Attributes:
        message (str): A human-readable description of the error.
        error_code (str): A machine-readable identifier for the error type.
        metadata (dict): Additional contextual information relevant to the
                         error.
        cause (Exception): Optional underlying exception that caused this
                           error.
    """

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        cause: Optional[Exception] = None,
    ) -> None:
        """
        Initialize a new SpaceGitException.

        Args:
            message (str): A user-friendly description of the error.
            error_code (Optional[str]): A custom error code to identify
                                        the issue.
                Defaults to "SPACE_GIT_ERROR" if not provided.
            metadata (Optional[Dict[str, Any]]): Contextual metadata (
                                                 e.g. space name, file path).
            cause (Optional[Exception]): Original exception causing the
                                         error, if any.
        """
        super().__init__(
            message=message,
            error_code=error_code or "SPACE_GIT_ERROR",
            metadata=metadata,
            cause=cause,
        )
