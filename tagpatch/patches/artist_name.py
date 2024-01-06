import pathlib
import shutil
import click
import music_tag
import mutagen
from tagpatch import utils
from tagpatch.patches import patch
from tagpatch.types import Table


class ArtistNamePatch(patch.Patch):
    _HELP_TEXT = "A patch which replaces existing delimiters in the `Artist` tag with the `/` seperator."
    TAG_NAME = "Artist"
    NEW_DELIMITER = "/"
    OLD_DELIMITERS = [",", "//", ";"]

    def __init__(self, src: pathlib.Path, dst: pathlib.Path, nested: bool):
        super().__init__()
        self.table: Table = []
        self.tracks = utils.get_tracks(
            src, dst, nested
        )  # [(absolute_src.mp3, absolute_dst.mp3), (), ...]

    @classmethod
    def help(cls) -> str:
        return cls._HELP_TEXT

    @classmethod
    def replace(cls, original: str) -> str:
        modified = original
        for delimiter in cls.OLD_DELIMITERS:
            seperated = modified.split(delimiter)
            modified = cls.NEW_DELIMITER.join([item.strip() for item in seperated])
        return modified

    def prepare(self) -> Table:
        table = []
        for track in self.tracks:
            src_file = track[0]
            dst_file = track[1]

            f: mutagen.FileType = music_tag.load_file(src_file)
            original_tag: str = str(f[self.TAG_NAME])
            modified_tag: str = self.replace(original_tag)
            colored_modified_tag = modified_tag
            if original_tag != modified_tag:
                colored_modified_tag = f"\033[31m{modified_tag}\033[0m"

            table.append([original_tag, colored_modified_tag, src_file, dst_file])
        self.table = table
        return table

    @property
    def table_headers(self) -> list[str]:
        return ["Original Tag", "Modified Tag", "Source", "Destination"]

    def apply(self) -> None:
        change_log: str = "\n"

        # Run with a progressbar.
        with click.progressbar(self.tracks) as bar:
            for track in bar:
                src_file = track[0]
                dst_file = track[1]

                try:
                    # If src_file is not equal to dst_file then copy src_file to dst_file first.
                    dst_file.touch()
                    if not src_file.samefile(dst_file):
                        shutil.copy2(src_file, dst_file)
                        change_log += f"Copied - {dst_file}\n"

                    # Change tags in dst_file.
                    f: mutagen.FileType = music_tag.load_file(dst_file)
                    original_tag: str = str(f[self.TAG_NAME])
                    modified_tag: str = self.replace(original_tag)
                    if original_tag != modified_tag:
                        f[self.TAG_NAME] = modified_tag
                        f.save()
                        change_log += f"Patched - {dst_file}\n"
                except Exception as e:
                    change_log += f"Error - failed to patch {dst_file}: {e}\n"

        # Print the changelog.
        click.echo(change_log)
