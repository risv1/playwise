import uuid
from datetime import datetime
from typing import Optional

class Song:
    """
    Song model for the PlayWise music playlist management engine.
    
    Time Complexity: O(1) for all operations
    Space Complexity: O(1) per song object
    """
    
    def __init__(self, title: str, artist: str, duration: int, rating: int = 0, song_id: Optional[str] = None):
        self.id = song_id or str(uuid.uuid4())
        self.title = title
        self.artist = artist
        self.duration = duration  # Duration in seconds
        self.rating = max(0, min(5, rating))  # Ensure rating is between 0-5
        self.date_added = datetime.now()
        self.listen_time = 0  # Total time listened in seconds
        self.play_count = 0

    def __repr__(self):
        return f"Song(id='{self.id}', title='{self.title}', artist='{self.artist}', duration={self.duration}, rating={self.rating})"
    
    def __eq__(self, other):
        if not isinstance(other, Song):
            return False
        return self.id == other.id
    
    def __hash__(self):
        return hash(self.id)

    def update_rating(self, new_rating: int):
        """Update song rating ensuring it stays within valid range."""
        self.rating = max(0, min(5, new_rating))

    def increment_play_count(self):
        """Increment the play count for analytics."""
        self.play_count += 1
    
    def add_listen_time(self, seconds: int):
        """Add to the total listen time."""
        self.listen_time += seconds

    def get_info(self) -> dict:
        """Get comprehensive song information."""
        return {
            'id': self.id,
            'title': self.title,
            'artist': self.artist,
            'duration': self.duration,
            'rating': self.rating,
            'date_added': self.date_added.isoformat(),
            'listen_time': self.listen_time,
            'play_count': self.play_count
        }
    
    def to_dict(self) -> dict:
        """Convert song to dictionary for API responses."""
        return self.get_info()