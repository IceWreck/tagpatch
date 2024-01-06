import pathlib
import shutil
import click
import music_tag
import mutagen
from tagpatch import utils
from tagpatch.patches import patch
from tagpatch.types import Table


class EmbedLyricsPatch(patch.Patch):
    _HELP_TEXT = "A patch which embeds .lrc files of the same name into the track file."
    TAG_NAME = "lyrics"

    def __init__(self, src: pathlib.Path, dst: pathlib.Path, nested: bool):
        super().__init__()
        self.table: Table = []
        self.tracks = utils.get_tracks(
            src, dst, nested
        )  # [(absolute_src.mp3, absolute_dst.mp3), (), ...]

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
        for track in self.tracks:
            src_file = track[0]
            dst_file = track[1]
            lrc_file = self.lrc_path(src_file)

            colored_lrc_path = ""
            if lrc_file is not None:
                colored_lrc_path = utils.ansi_colorify(lrc_file)

            self.table.append([colored_lrc_path, src_file, dst_file])
        return self.table

    @property
    def table_headers(self) -> list[str]:
        return ["Lyric File", "Source", "Destination"]

    def apply(self) -> None:
        change_log: str = "\n"

        # Run with a progressbar.
        with click.progressbar(self.tracks) as bar:
            for track in bar:
                src_file = track[0]
                dst_file = track[1]

                try:
                    lrc_file = self.lrc_path(src_file)

                    # If src_file is not equal to dst_file then copy src_file to dst_file first.
                    dst_file.touch()
                    if not src_file.samefile(dst_file):
                        shutil.copy2(src_file, dst_file)
                        change_log += f"Copied - {dst_file}\n"

                    # Read the .lrc file
                    modified_tag = ""
                    if lrc_file is not None:
                        with open(lrc_file, "r") as lrcf:
                            modified_tag = lrcf.read()

                    # Change tags in dst_file.
                    f: mutagen.FileType = music_tag.load_file(dst_file)
                    original_tag: str = str(f[self.TAG_NAME])
                    if original_tag != modified_tag:
                        f[self.TAG_NAME] = modified_tag
                        f.save()
                        change_log += f"Patched - {dst_file}\n"
                except Exception as e:
                    change_log += f"Error - failed to patch {dst_file}: {e}\n"

        # Print the changelog.
        click.echo(change_log)
