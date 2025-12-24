import dataclasses
import logging
import pathlib
from typing import cast

import httpx
import music_tag
import typer
from mutagen._file import File as MutagenFile

from tagpatch import utils
from tagpatch.patches import patch
from tagpatch.types import Table

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class _LyricChange:
    src: pathlib.Path
    skip_reason: str
    synced: bool
    lyrics: str | None


class DownloadLrcPatch(patch.Patch):
    _HELP_TEXT: str = "A patch which downloads .lrc files from lrclib.net if not present."

    API_BASE_URL: str = "https://lrclib.net/api/get"

    def __init__(self, src: pathlib.Path, nested: bool) -> None:
        super().__init__()
        self.tracks = utils.get_tracks(src, src, nested)
        self._changes: list[_LyricChange] = []

    @classmethod
    def help(cls) -> str:
        return cls._HELP_TEXT

    @staticmethod
    def get_metadata(src_file: pathlib.Path) -> dict[str, str | float | None]:
        """Extract metadata from audio file."""
        f = music_tag.load_file(src_file)
        artist_raw = str(f["artist"]).strip()
        album_raw = str(f["album"]).strip()
        title_raw = str(f["title"]).strip()

        artist = artist_raw if artist_raw else None
        album = album_raw if album_raw else None
        title = title_raw if title_raw else None

        duration = None
        mutagen_file = MutagenFile(src_file)
        if mutagen_file and mutagen_file.info:
            duration = mutagen_file.info.length

        return {"artist": artist, "album": album, "title": title, "duration": duration}

    @staticmethod
    def has_embedded_lyrics(src_file: pathlib.Path) -> bool:
        """Check if lyrics are embedded in the audio file."""
        f = music_tag.load_file(src_file)
        lyrics = str(f["lyrics"]).strip()
        return len(lyrics) > 0

    @staticmethod
    def has_lrc_file(src_file: pathlib.Path) -> bool:
        """Check if .lrc file exists."""
        lrc_file = src_file.with_suffix(".lrc")
        return lrc_file.exists()

    @staticmethod
    def has_txt_file(src_file: pathlib.Path) -> bool:
        """Check if .txt file exists."""
        txt_file = src_file.with_suffix(".txt")
        return txt_file.exists()

    @staticmethod
    def fetch_lyrics_from_lrclib(
        artist: str, title: str, album: str | None, duration: float | None
    ) -> tuple[str | None, str | None]:
        """Fetch lyrics from lrclib API. Returns (synced_lyrics, plain_lyrics)."""
        params: dict[str, str | int] = {"artist_name": artist, "track_name": title}
        if album:
            params["album_name"] = album
        if duration is not None:
            params["duration"] = int(round(duration))

        synced_lyrics = None
        plain_lyrics = None

        try:
            response = httpx.get(DownloadLrcPatch.API_BASE_URL, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()

            if isinstance(data, list):
                if data:
                    synced_lyrics = data[0].get("syncedLyrics")
                    plain_lyrics = data[0].get("plainLyrics")
            elif isinstance(data, dict):
                synced_lyrics = data.get("syncedLyrics")
                plain_lyrics = data.get("plainLyrics")

        except httpx.HTTPStatusError as e:
            logger.warning(f"http error fetching lyrics for {title} by {artist}: {e}")
        except Exception as e:
            logger.warning(f"error fetching lyrics for {title} by {artist}: {e}")

        return synced_lyrics, plain_lyrics

    def prepare(self) -> Table:
        table = []
        for track in self.tracks:
            src_file = track[0]

            metadata = self.get_metadata(src_file)
            artist = cast("str | None", metadata.get("artist"))
            title = cast("str | None", metadata.get("title"))
            album = cast("str | None", metadata.get("album"))
            duration = cast("float | None", metadata.get("duration"))

            skip_reason = ""
            action = ""
            lyric_type = ""

            synced_lyrics = None
            plain_lyrics = None
            synced = False

            if not artist or not title:
                skip_reason = "Missing metadata"
            elif self.has_lrc_file(src_file):
                skip_reason = ".lrc file exists"
            elif self.has_txt_file(src_file):
                skip_reason = ".txt file exists"
            elif self.has_embedded_lyrics(src_file):
                skip_reason = "Embedded lyrics"
            else:
                synced_lyrics, plain_lyrics = self.fetch_lyrics_from_lrclib(artist, title, album, duration)
                if synced_lyrics:
                    action = "Download"
                    lyric_type = "synced (.lrc)"
                    synced = True
                elif plain_lyrics:
                    action = "Download"
                    lyric_type = "plain (.txt)"
                    synced = False
                else:
                    skip_reason = "No lyrics found"

            self._changes.append(_LyricChange(
                src=src_file,
                skip_reason=skip_reason,
                synced=synced,
                lyrics=synced_lyrics if synced else plain_lyrics,
            ))

            dst_name = src_file.with_suffix(".lrc" if synced else ".txt").name if action else ""
            colored_action = utils.ansi_colorify(action if action else skip_reason)
            colored_type = utils.ansi_colorify(lyric_type) if lyric_type else ""

            table.append([src_file.name, dst_name, colored_action, colored_type])

        return table

    @property
    def table_headers(self) -> list[str]:
        return ["Source", "Destination", "Action", "Type"]

    def apply(self) -> None:
        change_log = "\n"

        for change in self._changes:
            if change.skip_reason:
                continue

            if not change.lyrics:
                continue

            try:
                if change.synced:
                    lrc_file = change.src.with_suffix(".lrc")
                    lrc_file.write_text(change.lyrics, encoding="utf-8")
                    change_log += f"Downloaded synced lyrics - {lrc_file}\n"
                else:
                    txt_file = change.src.with_suffix(".txt")
                    txt_file.write_text(change.lyrics, encoding="utf-8")
                    change_log += f"Downloaded plain lyrics - {txt_file}\n"
            except Exception as e:
                change_log += f"error - failed to save lyrics for {change.src}: {e}\n"

        typer.echo(change_log)
