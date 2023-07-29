import unittest
import pathlib
import music_tag
from tagpatch.patches import artist_name
from tagpatch import utils


class TestArtistName(unittest.TestCase):
    def setUp(self):
        self.src = pathlib.Path().cwd().resolve() / "tests/data"
        self.dst = pathlib.Path().cwd().resolve() / "tests/output"

    def test_replace(self):
        replacements = [
            ("Sigrid, Bring Me The Horizon", "Sigrid/Bring Me The Horizon"),
            ("Sigrid ; Bring Me The Horizon", "Sigrid/Bring Me The Horizon"),
            ("Sigrid//Bring Me The Horizon", "Sigrid/Bring Me The Horizon"),
            ("Sigrid/Bring Me The Horizon", "Sigrid/Bring Me The Horizon"),
            ("Sigrid ;Bring Me The Horizon", "Sigrid/Bring Me The Horizon"),
            ("Foo; bar, baz", "Foo/bar/baz"),
        ]

        for replacement in replacements:
            self.assertEqual(
                artist_name.ArtistNamePatch.replace(replacement[0]), replacement[1]
            )

    def test_artist_name_mock(self):
        patch = artist_name.ArtistNamePatch(self.src, self.dst, nested=True)
        table = patch.prepare()
        src_track_file = self.src / "song1/test.mp3"
        dst_track_file = self.dst / "test.mp3"
        self.assertEqual(len(table), 1)
        self.assertEqual("Cartoon, Daniel Levi", table[0][0])
        self.assertEqual("Cartoon/Daniel Levi", utils.escape_ansi(table[0][1]))
        self.assertEqual(src_track_file, table[0][2])
        self.assertEqual(dst_track_file, table[0][3])

    def test_artist_name_patch(self):
        patch = artist_name.ArtistNamePatch(self.src, self.dst, nested=True)
        table = patch.prepare()
        dst_track_file = self.dst / "test.mp3"
        patch.apply()

        f = music_tag.load_file(dst_track_file)
        tag: str = str(f["Artist"])
        self.assertEqual("Cartoon/Daniel Levi", tag)

    def tearDown(self):
        """Delete all .mp3 files in the tests/output directory."""
        for file in self.dst.iterdir():
            if file.suffix == ".mp3":
                file.unlink()


if __name__ == "__main__":
    unittest.main()
