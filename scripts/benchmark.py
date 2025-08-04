# Benchmarking script for PlayWise engine performance

import time
import random
from src.core.playlist_engine import PlaylistEngine
from src.core.playback_history import PlaybackHistory
from src.core.song_rating_tree import SongRatingTree
from src.core.song_lookup import SongLookup
from src.core.playlist_sorter import PlaylistSorter
from src.core.auto_cleaner import AutoCleaner
from src.core.favorites_queue import FavoritesQueue
from src.core.system_snapshot import SystemSnapshot

def benchmark_playlist_engine():
    print("Benchmarking Playlist Engine...")
    playlist = PlaylistEngine()
    
    # Add songs
    start_time = time.time()
    for i in range(1000):
        playlist.add_song(f"Song {i}", position=-1)
    print(f"Time to add 1000 songs: {time.time() - start_time:.4f} seconds")

    # Delete songs
    start_time = time.time()
    for i in range(500):
        playlist.delete_song(0)  # Always delete the first song
    print(f"Time to delete 500 songs: {time.time() - start_time:.4f} seconds")

def benchmark_playback_history():
    print("Benchmarking Playback History...")
    history = PlaybackHistory()
    
    # Add to history
    start_time = time.time()
    for i in range(100):
        history.add_to_history(f"Song {i}")
    print(f"Time to add 100 songs to history: {time.time() - start_time:.4f} seconds")

    # Undo last play
    start_time = time.time()
    for _ in range(50):
        history.undo_last_play()
    print(f"Time to undo 50 plays: {time.time() - start_time:.4f} seconds")

def benchmark_song_rating_tree():
    print("Benchmarking Song Rating Tree...")
    rating_tree = SongRatingTree()
    
    # Insert songs
    start_time = time.time()
    for i in range(1000):
        rating_tree.insert_song(f"Song {i}", random.randint(1, 5))
    print(f"Time to insert 1000 songs: {time.time() - start_time:.4f} seconds")

    # Search by rating
    start_time = time.time()
    rating_tree.search_by_rating(random.randint(1, 5))
    print(f"Time to search by rating: {time.time() - start_time:.4f} seconds")

def main():
    benchmark_playlist_engine()
    benchmark_playback_history()
    benchmark_song_rating_tree()

if __name__ == "__main__":
    main()