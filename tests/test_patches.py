import unittest
import pathlib
from tagpatch.patches import artist_name


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
            self.assertEqual(artist_name.ArtistNamePatch.replace(replacement[0]), replacement[1])

    def tearDown(self):
        """Delete all .mp3 files in the tests/output directory."""
        for file in self.dst.iterdir():
            if file.suffix == ".mp3":
                file.unlink()


if __name__ == "__main__":
    unittest.main()
