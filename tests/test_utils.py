import unittest
import pathlib
from tagpatch import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.src = pathlib.Path().cwd().resolve() / "tests/data"
        self.dst = pathlib.Path().cwd().resolve() / "tests/output"

    def test_get_tracks_nested_v1(self):
        """Test get_tracks where nested=True and src=tests/data."""
        tracks = utils.get_tracks(self.src, self.dst, nested=True)
        src_track_file = self.src / "song1/test.mp3"
        dst_track_file = self.dst / "test.mp3"
        self.assertEqual(src_track_file, tracks[0][0])
        self.assertEqual(dst_track_file, tracks[0][1])

    def test_get_tracks_nested_v2(self):
        """Test get_tracks where nested=True and src=dst=tests/data."""
        self.dst = self.src
        tracks = utils.get_tracks(self.src, self.dst, nested=True)
        src_track_file = self.src / "song1/test.mp3"
        dst_track_file = src_track_file
        self.assertEqual(src_track_file, tracks[0][0])
        self.assertEqual(dst_track_file, tracks[0][1])

    def test_get_tracks_v1(self):
        """Test get_tracks where nested=False and src=tests/data."""
        tracks = utils.get_tracks(self.src, self.dst, nested=False)
        self.assertEqual(len(tracks), 0)

    def test_get_tracks_v2(self):
        """Test get_tracks where nested=False and src=tests/data/song1."""
        self.src = self.src / "song1"

        tracks = utils.get_tracks(self.src, self.dst, nested=False)
        src_track_file = self.src / "test.mp3"
        dst_track_file = self.dst / "test.mp3"
        self.assertEqual(src_track_file, tracks[0][0])
        self.assertEqual(dst_track_file, tracks[0][1])


if __name__ == "__main__":
    unittest.main()
