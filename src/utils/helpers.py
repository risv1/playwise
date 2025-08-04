# This file contains utility functions that assist with various operations within the PlayWise engine.

def format_song_title(title):
    """Format the song title for display."""
    return title.title()

def calculate_average_rating(ratings):
    """Calculate the average rating from a list of ratings."""
    if not ratings:
        return 0
    return sum(ratings) / len(ratings)

def is_duplicate(song, song_list):
    """Check if a song is a duplicate in the given song list."""
    return any(existing_song.title.lower() == song.title.lower() and existing_song.artist.lower() == song.artist.lower() for existing_song in song_list)

def generate_unique_id(existing_ids):
    """Generate a unique ID not present in the existing IDs."""
    new_id = 1
    while new_id in existing_ids:
        new_id += 1
    return new_id