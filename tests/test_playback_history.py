import unittest
from src.core.playback_history import PlaybackHistory

class TestPlaybackHistory(unittest.TestCase):

    def setUp(self):
        self.history = PlaybackHistory(max_size=5)

    def test_add_to_history(self):
        self.history.add_to_history("Song A")
        self.history.add_to_history("Song B")
        self.assertEqual(self.history.get_recent_history(2), ["Song B", "Song A"])

    def test_undo_last_play(self):
        self.history.add_to_history("Song A")
        self.history.add_to_history("Song B")
        self.history.undo_last_play()
        self.assertEqual(self.history.get_recent_history(1), ["Song A"])

    def test_history_limit(self):
        for i in range(7):
            self.history.add_to_history(f"Song {i}")
        self.assertEqual(self.history.get_recent_history(5), ["Song 6", "Song 5", "Song 4", "Song 3", "Song 2"])

    def test_empty_history(self):
        self.assertEqual(self.history.get_recent_history(1), [])

if __name__ == '__main__':
    unittest.main()