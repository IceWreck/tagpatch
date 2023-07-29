from abc import ABC, abstractmethod
from tagpatch.types import Table


class Patch(ABC):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    @abstractmethod
    def help(cls) -> str:
        """Help text for the patch."""
        raise NotImplementedError

    @abstractmethod
    def prepare(self) -> Table:
        """Return a table of changes to be done without executing them."""
        raise NotImplementedError

    @abstractmethod
    def apply(self) -> None:
        """Apply the patch."""
        raise NotImplementedError

    @property
    @abstractmethod
    def table_headers(self) -> list:
        """Headers for the dry-run table."""
        raise NotImplementedError

    @property
    def table_format(self) -> str:
        return "grid"

    @property
    def table_max_col_width(self) -> int:
        return 30
