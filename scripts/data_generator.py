# Sample data generator for PlayWise music playlist management engine

import random
import string

def generate_random_song_title(length=10):
    """Generate a random song title."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_random_artist_name(length=8):
    """Generate a random artist name."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_sample_songs(num_songs=100):
    """Generate a list of sample songs."""
    songs = []
    for _ in range(num_songs):
        title = generate_random_song_title()
        artist = generate_random_artist_name()
        duration = random.randint(180, 300)  # Duration in seconds
        rating = random.randint(1, 5)  # Rating from 1 to 5
        songs.append({
            'title': title,
            'artist': artist,
            'duration': duration,
            'rating': rating
        })
    return songs

if __name__ == "__main__":
    sample_songs = generate_sample_songs(100)
    for song in sample_songs:
        print(song)