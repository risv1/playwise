import unittest
from src.core.song_rating_tree import SongRatingTree
from src.models.song import Song

class TestSongRatingTree(unittest.TestCase):

    def setUp(self):
        self.rating_tree = SongRatingTree()

    def test_insert_song(self):
        song = Song("Song Title", "Artist Name", 180, 5)
        self.rating_tree.insert_song(song, song.rating)
        self.assertIn(song, self.rating_tree.get_songs_by_rating_range(5, 5))

    def test_search_by_rating(self):
        song1 = Song("Song A", "Artist A", 200, 4)
        song2 = Song("Song B", "Artist B", 240, 5)
        self.rating_tree.insert_song(song1, song1.rating)
        self.rating_tree.insert_song(song2, song2.rating)
        result = self.rating_tree.search_by_rating(5)
        self.assertEqual(result, [song2])

    def test_delete_song(self):
        song = Song("Song Title", "Artist Name", 180, 5)
        self.rating_tree.insert_song(song, song.rating)
        self.rating_tree.delete_song(song.title)
        self.assertNotIn(song, self.rating_tree.get_songs_by_rating_range(5, 5))

    def test_get_songs_by_rating_range(self):
        song1 = Song("Song A", "Artist A", 200, 3)
        song2 = Song("Song B", "Artist B", 240, 5)
        self.rating_tree.insert_song(song1, song1.rating)
        self.rating_tree.insert_song(song2, song2.rating)
        result = self.rating_tree.get_songs_by_rating_range(3, 5)
        self.assertEqual(set(result), {song1, song2})

if __name__ == '__main__':
    unittest.main()