from darca_exception.exception import DarcaException


class SpaceGitException(DarcaException):
    """
    Exception raised for errors in the darca-space-git layer.
    Wraps git and space-related failures into a unified interface.
    """

    def __init__(self, message, error_code=None, metadata=None, cause=None):
        super().__init__(
            message=message,
            error_code=error_code or "SPACE_GIT_ERROR",
            metadata=metadata,
            cause=cause,
        )
