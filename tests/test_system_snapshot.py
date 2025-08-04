import unittest
from src.core.system_snapshot import SystemSnapshot

class TestSystemSnapshot(unittest.TestCase):

    def setUp(self):
        self.snapshot = SystemSnapshot()

    def test_generate_snapshot(self):
        # Assuming the SystemSnapshot class has a method to generate a snapshot
        result = self.snapshot.generate_snapshot()
        self.assertIsInstance(result, dict)  # Check if the result is a dictionary
        self.assertIn('top_longest_songs', result)  # Check for expected keys
        self.assertIn('recently_played', result)
        self.assertIn('rating_distribution', result)
        self.assertIn('playlist_statistics', result)

    def test_top_longest_songs(self):
        # Assuming the SystemSnapshot class has a method to get top longest songs
        top_songs = self.snapshot.get_top_longest_songs()
        self.assertIsInstance(top_songs, list)  # Check if the result is a list
        self.assertTrue(all(isinstance(song, dict) for song in top_songs))  # Check if each song is a dictionary

    def test_recently_played(self):
        recently_played = self.snapshot.get_recently_played()
        self.assertIsInstance(recently_played, list)  # Check if the result is a list
        self.assertTrue(all(isinstance(song, dict) for song in recently_played))  # Check if each song is a dictionary

    def test_rating_distribution(self):
        distribution = self.snapshot.get_rating_distribution()
        self.assertIsInstance(distribution, dict)  # Check if the result is a dictionary
        self.assertTrue(all(isinstance(key, int) for key in distribution.keys()))  # Check if keys are ratings
        self.assertTrue(all(isinstance(value, int) for value in distribution.values()))  # Check if values are counts

    def test_playlist_statistics(self):
        statistics = self.snapshot.get_playlist_statistics()
        self.assertIsInstance(statistics, dict)  # Check if the result is a dictionary
        self.assertIn('total_playlists', statistics)  # Check for expected keys
        self.assertIn('total_songs', statistics)

if __name__ == '__main__':
    unittest.main()