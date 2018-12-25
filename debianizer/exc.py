class DebianizerError(Exception):
    """Root exception."""


class PathError(DebianizerError):
    """Path root exception."""


class PathAlreadyExistsError(PathError):
    """Path already exists."""


class PathDoesNotExistsError(PathError):
    """Path does not exists."""


class SetupPyDoesNotFoundError(PathError):
    """setup.py does not found in project directory."""
