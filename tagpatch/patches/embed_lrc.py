import dataclasses
import pathlib
import shutil

import music_tag
import typer

from tagpatch import utils
from tagpatch.patches import patch
from tagpatch.types import Table


@dataclasses.dataclass
class _EmbedChange:
    src: pathlib.Path
    dst: pathlib.Path
    lrc_file: pathlib.Path | None


class EmbedLyricsPatch(patch.Patch):
    _HELP_TEXT: str = "A patch which embeds .lrc files of the same name into the track file."
    TAG_NAME: str = "lyrics"

    def __init__(self, src: pathlib.Path, dst: pathlib.Path, nested: bool) -> None:
        super().__init__()
        self.tracks = utils.get_tracks(src, dst, nested)
        self._changes: list[_EmbedChange] = []

    @classmethod
    def help(cls) -> str:
        return cls._HELP_TEXT

    @staticmethod
    def lrc_path(src_file: pathlib.Path) -> pathlib.Path | None:
        """Returns the path of lrc file for the corresponding src file, if exists."""
        if not src_file.is_file():
            raise ValueError("src_file parameter must be a file")
        lrc_file = src_file.with_suffix(".lrc").resolve()
        if lrc_file.exists():
            return lrc_file
        return None

    def prepare(self) -> Table:
        table = []
        for track in self.tracks:
            src_file = track[0]
            dst_file = track[1]
            lrc_file = self.lrc_path(src_file)

            self._changes.append(
                _EmbedChange(
                    src=src_file,
                    dst=dst_file,
                    lrc_file=lrc_file,
                )
            )

            colored_lrc_path = ""
            if lrc_file is not None:
                colored_lrc_path = utils.ansi_colorify(str(lrc_file))

            table.append([colored_lrc_path, src_file, dst_file])

        return table

    @property
    def table_headers(self) -> list[str]:
        return ["Lyric File", "Source", "Destination"]

    def apply(self) -> None:
        for change in self._changes:
            try:
                change.dst.touch()
                if not change.src.samefile(change.dst):
                    shutil.copy2(change.src, change.dst)
                    typer.echo(f"Copied - {change.dst}")

                modified_tag = ""
                if change.lrc_file is not None:
                    modified_tag = change.lrc_file.read_text()

                f = music_tag.load_file(change.dst)
                original_tag: str = str(f[self.TAG_NAME])
                if original_tag != modified_tag:
                    f[self.TAG_NAME] = modified_tag
                    f.save()
                    typer.echo(f"Patched - {change.dst}")
            except Exception as e:
                typer.echo(f"Error - failed to patch {change.dst}: {e}")
