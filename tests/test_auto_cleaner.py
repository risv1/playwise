import unittest
from src.core.auto_cleaner import AutoCleaner

class TestAutoCleaner(unittest.TestCase):

    def setUp(self):
        self.auto_cleaner = AutoCleaner()

    def test_remove_duplicates(self):
        songs = [
            {"title": "Song A", "artist": "Artist 1"},
            {"title": "Song B", "artist": "Artist 2"},
            {"title": "Song A", "artist": "Artist 1"},
        ]
        cleaned_songs = self.auto_cleaner.remove_duplicates(songs)
        self.assertEqual(len(cleaned_songs), 2)

    def test_find_duplicates(self):
        songs = [
            {"title": "Song A", "artist": "Artist 1"},
            {"title": "Song B", "artist": "Artist 2"},
            {"title": "Song A", "artist": "Artist 1"},
        ]
        duplicates = self.auto_cleaner.find_duplicates(songs)
        self.assertEqual(len(duplicates), 1)
        self.assertEqual(duplicates[0], {"title": "Song A", "artist": "Artist 1"})

if __name__ == '__main__':
    unittest.main()