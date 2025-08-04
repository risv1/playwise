import unittest
from src.core.playlist_sorter import PlaylistSorter

class TestPlaylistSorter(unittest.TestCase):

    def setUp(self):
        self.sorter = PlaylistSorter()

    def test_sort_by_title(self):
        songs = [
            {"title": "Song B", "duration": 210},
            {"title": "Song A", "duration": 180},
            {"title": "Song C", "duration": 240}
        ]
        sorted_songs = self.sorter.sort_by_title(songs)
        self.assertEqual(sorted_songs[0]["title"], "Song A")
        self.assertEqual(sorted_songs[1]["title"], "Song B")
        self.assertEqual(sorted_songs[2]["title"], "Song C")

    def test_sort_by_duration(self):
        songs = [
            {"title": "Song A", "duration": 180},
            {"title": "Song B", "duration": 210},
            {"title": "Song C", "duration": 240}
        ]
        sorted_songs = self.sorter.sort_by_duration(songs)
        self.assertEqual(sorted_songs[0]["duration"], 180)
        self.assertEqual(sorted_songs[1]["duration"], 210)
        self.assertEqual(sorted_songs[2]["duration"], 240)

    def test_sort_by_date_added(self):
        songs = [
            {"title": "Song A", "date_added": "2023-01-01"},
            {"title": "Song B", "date_added": "2023-01-03"},
            {"title": "Song C", "date_added": "2023-01-02"}
        ]
        sorted_songs = self.sorter.sort_by_date_added(songs)
        self.assertEqual(sorted_songs[0]["title"], "Song A")
        self.assertEqual(sorted_songs[1]["title"], "Song C")
        self.assertEqual(sorted_songs[2]["title"], "Song B")

if __name__ == '__main__':
    unittest.main()