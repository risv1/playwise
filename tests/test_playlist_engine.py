import unittest
from src.core.playlist_engine import PlaylistEngine
from src.models.song import Song

class TestPlaylistEngine(unittest.TestCase):

    def setUp(self):
        self.playlist_engine = PlaylistEngine()
        self.song1 = Song("Song Title 1", "Artist 1", 210, 5)
        self.song2 = Song("Song Title 2", "Artist 2", 180, 4)
        self.song3 = Song("Song Title 3", "Artist 3", 240, 3)

    def test_add_song(self):
        self.playlist_engine.add_song(self.song1)
        self.assertIn(self.song1, self.playlist_engine.songs)

    def test_delete_song(self):
        self.playlist_engine.add_song(self.song1)
        self.playlist_engine.delete_song(0)
        self.assertNotIn(self.song1, self.playlist_engine.songs)

    def test_move_song(self):
        self.playlist_engine.add_song(self.song1)
        self.playlist_engine.add_song(self.song2)
        self.playlist_engine.move_song(0, 1)
        self.assertEqual(self.playlist_engine.songs[1], self.song1)

    def test_reverse_playlist(self):
        self.playlist_engine.add_song(self.song1)
        self.playlist_engine.add_song(self.song2)
        self.playlist_engine.reverse_playlist()
        self.assertEqual(self.playlist_engine.songs[0], self.song2)

if __name__ == '__main__':
    unittest.main()