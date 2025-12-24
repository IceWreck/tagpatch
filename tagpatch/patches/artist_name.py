import dataclasses
import pathlib
import shutil

import music_tag
import typer

from tagpatch import utils
from tagpatch.patches import patch
from tagpatch.types import Table


@dataclasses.dataclass
class _ArtistChange:
    src: pathlib.Path
    dst: pathlib.Path
    original: str
    modified: str
    has_change: bool


class ArtistNamePatch(patch.Patch):
    _HELP_TEXT = "A patch which replaces existing delimiters in the `Artist` tag with the `/` separator."
    TAG_NAME = "Artist"
    NEW_DELIMITER = "/"
    OLD_DELIMITERS = [",", "//", ";"]

    def __init__(self, src: pathlib.Path, dst: pathlib.Path, nested: bool):
        super().__init__()
        self.tracks = utils.get_tracks(src, dst, nested)
        self._changes: list[_ArtistChange] = []

    @classmethod
    def help(cls) -> str:
        return cls._HELP_TEXT

    @classmethod
    def replace(cls, original: str) -> str:
        modified = original
        for delimiter in cls.OLD_DELIMITERS:
            separated = modified.split(delimiter)
            modified = cls.NEW_DELIMITER.join([item.strip() for item in separated])
        return modified

    def prepare(self) -> Table:
        table = []
        for track in self.tracks:
            src_file = track[0]
            dst_file = track[1]

            f = music_tag.load_file(src_file)
            original_tag: str = str(f[self.TAG_NAME])
            modified_tag: str = self.replace(original_tag)

            colored_modified_tag = modified_tag
            if original_tag != modified_tag:
                colored_modified_tag = f"\033[31m{modified_tag}\033[0m"

            self._changes.append(_ArtistChange(
                src=src_file,
                dst=dst_file,
                original=original_tag,
                modified=modified_tag,
                has_change=original_tag != modified_tag,
            ))

            table.append([original_tag, colored_modified_tag, src_file, dst_file])

        return table

    @property
    def table_headers(self) -> list[str]:
        return ["Original Tag", "Modified Tag", "Source", "Destination"]

    def apply(self) -> None:
        change_log: str = "\n"

        for change in self._changes:
            if not change.has_change:
                continue

            try:
                change.dst.touch()
                if not change.src.samefile(change.dst):
                    shutil.copy2(change.src, change.dst)
                    change_log += f"Copied - {change.dst}\n"

                f = music_tag.load_file(change.dst)
                f[self.TAG_NAME] = change.modified
                f.save()
                change_log += f"Patched - {change.dst}\n"
            except Exception as e:
                change_log += f"Error - failed to patch {change.dst}: {e}\n"

        typer.echo(change_log)
