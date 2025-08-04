# Performance Tests for PlayWise Engine

import time
import random
from src.core.playlist_engine import PlaylistEngine
from src.models.song import Song

def generate_random_songs(num_songs):
    """Generate a list of random songs."""
    songs = []
    for i in range(num_songs):
        song = Song(title=f"Song {i}", artist=f"Artist {random.randint(1, 10)}", duration=random.randint(180, 300), rating=random.randint(1, 5))
        songs.append(song)
    return songs

def performance_test_playlist_engine():
    """Test the performance of the PlaylistEngine."""
    print("Starting performance tests for PlaylistEngine...")
    
    playlist = PlaylistEngine()
    num_songs = 1000
    songs = generate_random_songs(num_songs)

    # Measure time to add songs
    start_time = time.time()
    for song in songs:
        playlist.add_song(song)
    end_time = time.time()
    print(f"Time to add {num_songs} songs: {end_time - start_time:.4f} seconds")

    # Measure time to delete songs
    start_time = time.time()
    for i in range(num_songs // 2):  # Delete half of the songs
        playlist.delete_song(0)  # Always delete the first song
    end_time = time.time()
    print(f"Time to delete {num_songs // 2} songs: {end_time - start_time:.4f} seconds")

    # Measure time to reorder songs
    start_time = time.time()
    playlist.reverse_playlist()
    end_time = time.time()
    print(f"Time to reverse playlist: {end_time - start_time:.4f} seconds")

if __name__ == "__main__":
    performance_test_playlist_engine()