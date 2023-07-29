import pathlib
import re
import click

KNOWN_TRACK_EXTENSIONS = {".ogg", ".mp3", ".m4a", ".flac", ".opus", ".wav"}


def get_tracks(
    src: pathlib.Path, dst: pathlib.Path, nested: bool = False
) -> list[tuple[pathlib.Path, pathlib.Path]]:
    """
    Get a list of source and destination absolute paths for track files.
    Input params src and dst must be both files or both directories.
    """
    if not ((src.is_dir() and dst.is_dir()) or (src.is_file() and dst.is_file())):
        raise ValueError(
            "Source and destination must be both files or both directories."
        )

    tracks: list[tuple[pathlib.Path, pathlib.Path]] = []

    if src.is_dir():
        if nested:
            files_list = pathlib.Path(src).rglob("*")
        else:
            files_list = pathlib.Path(src).iterdir()

        overwrite_src: bool = src.samefile(dst)

        for file in files_list:
            if file.is_file() and file.suffix in KNOWN_TRACK_EXTENSIONS:
                # Since we may be looking in nested dirs, if src = dst overwrite original files.
                # If not then place all new files in dst directory.
                # Note that if src != dst and nested = True there may be a situation where both
                # `src/foo/song.mp3` and `src/bar/song.mp3` will be written to `dst/song.mp3`.
                if overwrite_src:
                    tracks.append((file.resolve(), file.resolve().parent / file.name))
                else:
                    tracks.append((file.resolve(), dst.resolve() / file.name))
    else:
        tracks.append((src.resolve(), dst.resolve()))

    return tracks


def escape_ansi(line):
    """Remove ANSI color codes from text."""
    ansi_escape = re.compile(r"(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", line)


def ansi_colorify(line):
    """Change the color of the line to red."""
    return f"\033[31m{line}\033[0m"


def prepare_src_dst(
    src: pathlib.Path, dst: pathlib.Path | None
) -> tuple[pathlib.Path, pathlib.Path]:
    """Basic checks and preparation before using the source and destination."""
    # If destination isn't provided, then make it equal to the source.
    if dst is None:
        dst = src
    # Create destination if it doesn't exist.
    if not dst.exists():
        if dst.suffix == "":
            # It is a directory.
            dst.mkdir(parents=True, exist_ok=True)
        else:
            # It is a file.
            dst.touch()
    # Source and destination must be of the same type.
    if not ((src.is_dir() and dst.is_dir()) or (src.is_file() and dst.is_file())):
        raise click.BadParameter(
            "Source and destination must be both files or both directories."
        )
    return src, dst
