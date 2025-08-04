"""
Playback History using Stack implementation
Tracks recently played songs with undo functionality
"""

from typing import List, Optional
from models.song import Song

class PlaybackHistory:
    """
    Stack-based playback history for undo functionality.
    
    Time Complexity:
    - Add to history: O(1)
    - Undo last play: O(1)
    - Get recent history: O(k) where k is requested items
    
    Space Complexity: O(h) where h is max_size
    """
    
    def __init__(self, max_size: int = 100):
        self.history: List[Song] = []
        self.max_size = max_size
    
    def add_to_history(self, song: Song) -> None:
        """
        Add a song to the playback history.
        
        Args:
            song: Song object to add to history
            
        Time Complexity: O(1)
        """
        # Remove oldest song if at max capacity
        if len(self.history) >= self.max_size:
            self.history.pop(0)  # Remove from front (oldest)
        
        self.history.append(song)
        
        # Update song statistics
        song.increment_play_count()
    
    def undo_last_play(self) -> Optional[Song]:
        """
        Remove and return the last played song.
        
        Returns:
            Song: Last played song or None if history is empty
            
        Time Complexity: O(1)
        """
        if self.history:
            return self.history.pop()
        return None
    
    def get_recent_history(self, k: int) -> List[Song]:
        """
        Get the k most recently played songs.
        
        Args:
            k: Number of recent songs to retrieve
            
        Returns:
            List[Song]: List of recent songs (most recent first)
            
        Time Complexity: O(k)
        """
        if k <= 0:
            return []
        
        # Return reversed to show most recent first
        return list(reversed(self.history[-k:]))
    
    def get_all_history(self) -> List[Song]:
        """
        Get complete playback history.
        
        Returns:
            List[Song]: All songs in history (most recent first)
        """
        return list(reversed(self.history))
    
    def clear_history(self) -> None:
        """Clear all playback history."""
        self.history.clear()
    
    def get_history_size(self) -> int:
        """Get current number of songs in history."""
        return len(self.history)
    
    def is_empty(self) -> bool:
        """Check if history is empty."""
        return len(self.history) == 0
    
    def get_most_played_songs(self, limit: int = 10) -> List[Song]:
        """
        Get most played songs from history based on play count.
        
        Args:
            limit: Maximum number of songs to return
            
        Returns:
            List[Song]: Songs sorted by play count (descending)
        """
        # Get unique songs and sort by play count
        unique_songs = {}
        for song in self.history:
            if song.id not in unique_songs:
                unique_songs[song.id] = song
        
        sorted_songs = sorted(
            unique_songs.values(),
            key=lambda s: s.play_count,
            reverse=True
        )
        
        return sorted_songs[:limit]
    
    def get_recently_played_artists(self, limit: int = 10) -> List[str]:
        """Get recently played artists."""
        artists = []
        seen = set()
        
        for song in reversed(self.history):
            if song.artist not in seen:
                artists.append(song.artist)
                seen.add(song.artist)
                if len(artists) >= limit:
                    break
        
        return artists