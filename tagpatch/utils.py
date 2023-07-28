import pathlib

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

    tracks = []

    if src.is_dir():
        if nested:
            files_list = pathlib.Path(src).rglob("*")
        else:
            files_list = pathlib.Path(src).iterdir()

        overwrite_src: bool = src.samefile(dst)

        for file in files_list:
            if file.is_file() and file.suffix in KNOWN_TRACK_EXTENSIONS:
                # Since we're looking in nested dirs, if src = dst overwrite og files.
                # If not then place all new files in dst directory.
                if overwrite_src:
                    tracks.append((file.resolve(), file.resolve().parent / file.name))
                else:
                    tracks.append((file.resolve(), dst.resolve() / file.name))
    else:
        tracks.append((src.resolve(), dst.resolve()))

    return tracks
