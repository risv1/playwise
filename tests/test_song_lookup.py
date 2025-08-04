import unittest
from src.core.song_lookup import SongLookup
from src.models.song import Song

class TestSongLookup(unittest.TestCase):

    def setUp(self):
        self.song_lookup = SongLookup()
        self.song1 = Song("Song Title 1", "Artist 1", 210, 5)
        self.song2 = Song("Song Title 2", "Artist 2", 180, 4)
        self.song3 = Song("Song Title 3", "Artist 1", 240, 3)
        self.song_lookup.add_song(self.song1)
        self.song_lookup.add_song(self.song2)
        self.song_lookup.add_song(self.song3)

    def test_get_song_by_id(self):
        self.assertEqual(self.song_lookup.get_song(self.song1.id), self.song1)
        self.assertEqual(self.song_lookup.get_song(self.song2.id), self.song2)

    def test_search_by_title(self):
        results = self.song_lookup.search_by_title("Song Title 1")
        self.assertIn(self.song1, results)
        self.assertNotIn(self.song2, results)

    def test_search_by_artist(self):
        results = self.song_lookup.search_by_artist("Artist 1")
        self.assertIn(self.song1, results)
        self.assertIn(self.song3, results)
        self.assertNotIn(self.song2, results)

    def test_add_duplicate_song(self):
        self.song_lookup.add_song(self.song1)
        self.assertEqual(len(self.song_lookup.songs), 3)  # Should not increase

    def tearDown(self):
        self.song_lookup.clear()  # Assuming there's a method to clear the lookup

if __name__ == '__main__':
    unittest.main()