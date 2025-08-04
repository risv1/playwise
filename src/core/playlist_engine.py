"""
Playlist Engine using Doubly Linked List implementation
Manages ordered song collections with efficient insertion, deletion, and reordering
"""

from typing import List, Optional, Dict
from models.song import Song
from models.playlist import Playlist

class PlaylistNode:
    """Node for doubly linked list implementation"""
    
    def __init__(self, song: Song):
        self.song = song
        self.next: Optional['PlaylistNode'] = None
        self.prev: Optional['PlaylistNode'] = None

class PlaylistEngine:
    """
    Manages playlists using doubly linked list for efficient operations.
    
    Time Complexity:
    - Add song: O(1) at head/tail, O(n) at arbitrary position
    - Delete song: O(1) with node reference, O(n) by index
    - Move song: O(n) (need to find positions)
    - Reverse: O(n)
    
    Space Complexity: O(n) where n is number of songs
    """
    
    def __init__(self):
        self.playlists: Dict[str, Playlist] = {}
        self.current_playlist_id: Optional[str] = None
    
    def create_playlist(self, name: str, description: str = "") -> str:
        """Create a new playlist and return its ID."""
        playlist = Playlist(name, description)
        self.playlists[playlist.id] = playlist
        if not self.current_playlist_id:
            self.current_playlist_id = playlist.id
        return playlist.id
    
    def get_playlist(self, playlist_id: str) -> Optional[Playlist]:
        """Get playlist by ID."""
        return self.playlists.get(playlist_id)
    
    def get_current_playlist(self) -> Optional[Playlist]:
        """Get the currently active playlist."""
        if self.current_playlist_id:
            return self.playlists.get(self.current_playlist_id)
        return None
    
    def set_current_playlist(self, playlist_id: str) -> bool:
        """Set the current active playlist."""
        if playlist_id in self.playlists:
            self.current_playlist_id = playlist_id
            return True
        return False
    
    def list_playlists(self) -> List[Playlist]:
        """Get all playlists."""
        return list(self.playlists.values())
    
    def delete_playlist(self, playlist_id: str) -> bool:
        """Delete a playlist."""
        if playlist_id in self.playlists:
            del self.playlists[playlist_id]
            if self.current_playlist_id == playlist_id:
                self.current_playlist_id = next(iter(self.playlists), None)
            return True
        return False
    
    def add_song(self, song: Song, position: int = -1, playlist_id: Optional[str] = None) -> bool:
        """
        Add a song to the specified playlist (or current playlist).
        
        Time Complexity: O(1) for append, O(n) for specific position
        """
        target_playlist = self._get_target_playlist(playlist_id)
        if target_playlist:
            return target_playlist.add_song(song, position)
        return False
    
    def delete_song(self, index: int, playlist_id: Optional[str] = None) -> Optional[Song]:
        """
        Delete a song at the specified index.
        
        Time Complexity: O(n)
        """
        target_playlist = self._get_target_playlist(playlist_id)
        if target_playlist:
            return target_playlist.remove_song(index)
        return None
    
    def move_song(self, from_idx: int, to_idx: int, playlist_id: Optional[str] = None) -> bool:
        """
        Move a song from one index to another.
        
        Time Complexity: O(n)
        """
        target_playlist = self._get_target_playlist(playlist_id)
        if target_playlist:
            return target_playlist.move_song(from_idx, to_idx)
        return False
    
    def reverse_playlist(self, playlist_id: Optional[str] = None) -> bool:
        """
        Reverse the order of songs in the playlist.
        
        Time Complexity: O(n)
        """
        target_playlist = self._get_target_playlist(playlist_id)
        if target_playlist:
            target_playlist.reverse_playlist()
            return True
        return False
    
    def get_songs(self, playlist_id: Optional[str] = None) -> List[Song]:
        """Get all songs from the specified playlist."""
        target_playlist = self._get_target_playlist(playlist_id)
        return target_playlist.songs if target_playlist else []
    
    def get_song_count(self, playlist_id: Optional[str] = None) -> int:
        """Get the number of songs in the playlist."""
        target_playlist = self._get_target_playlist(playlist_id)
        return len(target_playlist) if target_playlist else 0
    
    def find_song_by_id(self, song_id: str, playlist_id: Optional[str] = None) -> Optional[int]:
        """Find song index by ID in the specified playlist."""
        target_playlist = self._get_target_playlist(playlist_id)
        if target_playlist:
            return target_playlist.find_song_by_id(song_id)
        return None
    
    def _get_target_playlist(self, playlist_id: Optional[str] = None) -> Optional[Playlist]:
        """Get the target playlist (specified or current)."""
        if playlist_id:
            return self.playlists.get(playlist_id)
        elif self.current_playlist_id:
            return self.playlists.get(self.current_playlist_id)
        return None
    
    def clear_playlist(self, playlist_id: Optional[str] = None) -> bool:
        """Clear all songs from the specified playlist."""
        target_playlist = self._get_target_playlist(playlist_id)
        if target_playlist:
            target_playlist.songs.clear()
            return True
        return False
    
    def get_total_duration(self, playlist_id: Optional[str] = None) -> int:
        """Get total duration of the playlist in seconds."""
        target_playlist = self._get_target_playlist(playlist_id)
        return target_playlist.get_total_duration() if target_playlist else 0
