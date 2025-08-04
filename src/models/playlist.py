"""
Playlist model for managing collections of songs
"""

import uuid
from datetime import datetime
from typing import List, Optional
from .song import Song

class Playlist:
    """
    Playlist model that manages a collection of songs.
    
    Time Complexity: 
    - Add/Remove song: O(1) for append, O(n) for specific position
    - Search: O(n)
    - Access by index: O(1)
    
    Space Complexity: O(n) where n is the number of songs
    """
    
    def __init__(self, name: str, description: str = "", playlist_id: Optional[str] = None):
        self.id = playlist_id or str(uuid.uuid4())
        self.name = name
        self.description = description
        self.songs: List[Song] = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def __len__(self):
        return len(self.songs)
    
    def __getitem__(self, index):
        return self.songs[index]
    
    def __repr__(self):
        return f"Playlist(id='{self.id}', name='{self.name}', songs={len(self.songs)})"
    
    def add_song(self, song: Song, position: int = -1) -> bool:
        """
        Add a song to the playlist at the specified position.
        
        Args:
            song: Song object to add
            position: Position to insert (-1 for end)
            
        Returns:
            bool: True if added successfully
            
        Time Complexity: O(1) for append, O(n) for specific position
        """
        try:
            if position == -1 or position >= len(self.songs):
                self.songs.append(song)
            else:
                self.songs.insert(max(0, position), song)
            self.updated_at = datetime.now()
            return True
        except Exception:
            return False
    
    def remove_song(self, index: int) -> Optional[Song]:
        """
        Remove a song at the specified index.
        
        Args:
            index: Index of song to remove
            
        Returns:
            Song: Removed song object or None if invalid index
            
        Time Complexity: O(n)
        """
        if 0 <= index < len(self.songs):
            removed_song = self.songs.pop(index)
            self.updated_at = datetime.now()
            return removed_song
        return None
    
    def move_song(self, from_index: int, to_index: int) -> bool:
        """
        Move a song from one position to another.
        
        Args:
            from_index: Current position of the song
            to_index: Target position
            
        Returns:
            bool: True if moved successfully
            
        Time Complexity: O(n)
        """
        if 0 <= from_index < len(self.songs) and 0 <= to_index < len(self.songs):
            song = self.songs.pop(from_index)
            self.songs.insert(to_index, song)
            self.updated_at = datetime.now()
            return True
        return False
    
    def reverse_playlist(self):
        """
        Reverse the order of songs in the playlist.
        
        Time Complexity: O(n)
        """
        self.songs.reverse()
        self.updated_at = datetime.now()
    
    def get_total_duration(self) -> int:
        """Get total duration of all songs in seconds."""
        return sum(song.duration for song in self.songs)
    
    def find_song_by_id(self, song_id: str) -> Optional[int]:
        """Find song index by ID."""
        for i, song in enumerate(self.songs):
            if song.id == song_id:
                return i
        return None
    
    def get_songs_by_rating(self, min_rating: int = 0, max_rating: int = 5) -> List[Song]:
        """Get songs within a rating range."""
        return [song for song in self.songs if min_rating <= song.rating <= max_rating]
    
    def to_dict(self) -> dict:
        """Convert playlist to dictionary for API responses."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'songs': [song.to_dict() for song in self.songs],
            'total_duration': self.get_total_duration(),
            'song_count': len(self.songs),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
