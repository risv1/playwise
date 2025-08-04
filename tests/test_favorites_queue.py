import unittest
from src.core.favorites_queue import FavoritesQueue

class TestFavoritesQueue(unittest.TestCase):

    def setUp(self):
        self.favorites_queue = FavoritesQueue()

    def test_add_song(self):
        self.favorites_queue.add_song("Song A", listen_time=120)
        self.assertEqual(self.favorites_queue.get_top_songs(1)[0]['title'], "Song A")

    def test_update_listen_time(self):
        self.favorites_queue.add_song("Song B", listen_time=150)
        self.favorites_queue.update_listen_time("Song B", 200)
        self.assertEqual(self.favorites_queue.get_top_songs(1)[0]['title'], "Song B")

    def test_get_top_songs(self):
        self.favorites_queue.add_song("Song C", listen_time=100)
        self.favorites_queue.add_song("Song D", listen_time=300)
        top_songs = self.favorites_queue.get_top_songs(2)
        self.assertEqual(len(top_songs), 2)
        self.assertEqual(top_songs[0]['title'], "Song D")
        self.assertEqual(top_songs[1]['title'], "Song C")

    def test_empty_queue(self):
        top_songs = self.favorites_queue.get_top_songs(5)
        self.assertEqual(top_songs, [])

if __name__ == '__main__':
    unittest.main()