"""
Song Lookup using HashMap implementation
Provides instant retrieval of songs by ID, title, or artist
"""

from typing import Dict, List, Optional, Set
from models.song import Song

class SongLookup:
    """
    HashMap-based song lookup system for O(1) average case lookups.
    Maintains three hash tables for different lookup keys.
    
    Time Complexity:
    - Add song: O(1) average
    - Get song: O(1) average
    - Search: O(1) average for exact match, O(k) for multiple matches
    - Remove song: O(1) average
    
    Space Complexity: O(3n) where n is number of songs
    """
    
    def __init__(self):
        # Primary lookup by song ID
        self.songs_by_id: Dict[str, Song] = {}
        
        # Secondary lookups (can have multiple songs per key)
        self.songs_by_title: Dict[str, List[Song]] = {}
        self.songs_by_artist: Dict[str, List[Song]] = {}
        
        # For efficient fuzzy search
        self.all_songs: Set[Song] = set()
    
    def add_song(self, song: Song) -> bool:
        """
        Add a song to all lookup tables.
        
        Args:
            song: Song object to add
            
        Returns:
            bool: True if added, False if already exists
            
        Time Complexity: O(1) average
        """
        if song.id in self.songs_by_id:
            return False  # Song already exists
        
        # Add to primary lookup
        self.songs_by_id[song.id] = song
        
        # Add to secondary lookups
        self._add_to_title_lookup(song)
        self._add_to_artist_lookup(song)
        
        # Add to set for efficient operations
        self.all_songs.add(song)
        
        return True
    
    def _add_to_title_lookup(self, song: Song) -> None:
        """Add song to title lookup table."""
        title_key = song.title.lower().strip()
        if title_key not in self.songs_by_title:
            self.songs_by_title[title_key] = []
        self.songs_by_title[title_key].append(song)
    
    def _add_to_artist_lookup(self, song: Song) -> None:
        """Add song to artist lookup table."""
        artist_key = song.artist.lower().strip()
        if artist_key not in self.songs_by_artist:
            self.songs_by_artist[artist_key] = []
        self.songs_by_artist[artist_key].append(song)
    
    def get_song(self, song_id: str) -> Optional[Song]:
        """
        Retrieve a song by its ID.
        
        Args:
            song_id: ID of the song to retrieve
            
        Returns:
            Song: Song object or None if not found
            
        Time Complexity: O(1) average
        """
        return self.songs_by_id.get(song_id)
    
    def search_by_title(self, title: str) -> List[Song]:
        """
        Search for songs by title (exact match, case-insensitive).
        
        Args:
            title: Title to search for
            
        Returns:
            List[Song]: Songs with matching title
            
        Time Complexity: O(1) average for lookup, O(k) for result
        """
        title_key = title.lower().strip()
        return self.songs_by_title.get(title_key, []).copy()
    
    def search_by_artist(self, artist: str) -> List[Song]:
        """
        Search for songs by artist (exact match, case-insensitive).
        
        Args:
            artist: Artist to search for
            
        Returns:
            List[Song]: Songs by the specified artist
            
        Time Complexity: O(1) average for lookup, O(k) for result
        """
        artist_key = artist.lower().strip()
        return self.songs_by_artist.get(artist_key, []).copy()
    
    def fuzzy_search_title(self, query: str) -> List[Song]:
        """
        Fuzzy search for songs by title (partial matching).
        
        Args:
            query: Search query
            
        Returns:
            List[Song]: Songs with titles containing the query
            
        Time Complexity: O(n) where n is number of unique titles
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        results = []
        for title_key, songs in self.songs_by_title.items():
            if query_lower in title_key:
                results.extend(songs)
        
        return results
    
    def fuzzy_search_artist(self, query: str) -> List[Song]:
        """
        Fuzzy search for songs by artist (partial matching).
        
        Args:
            query: Search query
            
        Returns:
            List[Song]: Songs by artists containing the query
            
        Time Complexity: O(n) where n is number of unique artists
        """
        query_lower = query.lower().strip()
        if not query_lower:
            return []
        
        results = []
        for artist_key, songs in self.songs_by_artist.items():
            if query_lower in artist_key:
                results.extend(songs)
        
        return results
    
    def search_by_partial_info(self, title_query: Optional[str] = None, 
                              artist_query: Optional[str] = None) -> List[Song]:
        """
        Search by partial title and/or artist information.
        
        Args:
            title_query: Partial title to search for
            artist_query: Partial artist to search for
            
        Returns:
            List[Song]: Songs matching the criteria
        """
        title_results = set()
        artist_results = set()
        
        if title_query:
            title_results = set(self.fuzzy_search_title(title_query))
        
        if artist_query:
            artist_results = set(self.fuzzy_search_artist(artist_query))
        
        if title_query and artist_query:
            # Both criteria must match (intersection)
            return list(title_results & artist_results)
        elif title_query:
            return list(title_results)
        elif artist_query:
            return list(artist_results)
        else:
            return []
    
    def remove_song(self, song: Song) -> bool:
        """
        Remove a song from all lookup tables.
        
        Args:
            song: Song object to remove
            
        Returns:
            bool: True if removed, False if not found
            
        Time Complexity: O(1) average
        """
        if song.id not in self.songs_by_id:
            return False
        
        # Remove from primary lookup
        del self.songs_by_id[song.id]
        
        # Remove from secondary lookups
        self._remove_from_title_lookup(song)
        self._remove_from_artist_lookup(song)
        
        # Remove from set
        self.all_songs.discard(song)
        
        return True
    
    def _remove_from_title_lookup(self, song: Song) -> None:
        """Remove song from title lookup table."""
        title_key = song.title.lower().strip()
        if title_key in self.songs_by_title:
            try:
                self.songs_by_title[title_key].remove(song)
                if not self.songs_by_title[title_key]:
                    del self.songs_by_title[title_key]
            except ValueError:
                pass  # Song not in list
    
    def _remove_from_artist_lookup(self, song: Song) -> None:
        """Remove song from artist lookup table."""
        artist_key = song.artist.lower().strip()
        if artist_key in self.songs_by_artist:
            try:
                self.songs_by_artist[artist_key].remove(song)
                if not self.songs_by_artist[artist_key]:
                    del self.songs_by_artist[artist_key]
            except ValueError:
                pass  # Song not in list
    
    def update_song(self, song: Song) -> bool:
        """
        Update a song in the lookup tables.
        This removes and re-adds the song to handle key changes.
        
        Args:
            song: Updated song object
            
        Returns:
            bool: True if updated successfully
        """
        # Get the existing song
        old_song = self.songs_by_id.get(song.id)
        if not old_song:
            return False
        
        # Remove old version
        self.remove_song(old_song)
        
        # Add new version
        return self.add_song(song)
    
    def get_all_songs(self) -> List[Song]:
        """Get all songs in the lookup system."""
        return list(self.all_songs)
    
    def get_all_titles(self) -> List[str]:
        """Get all unique song titles."""
        return list(self.songs_by_title.keys())
    
    def get_all_artists(self) -> List[str]:
        """Get all unique artists."""
        return list(self.songs_by_artist.keys())
    
    def get_song_count(self) -> int:
        """Get total number of songs."""
        return len(self.songs_by_id)
    
    def clear(self) -> None:
        """Clear all lookup tables."""
        self.songs_by_id.clear()
        self.songs_by_title.clear()
        self.songs_by_artist.clear()
        self.all_songs.clear()
    
    def get_stats(self) -> Dict[str, int]:
        """Get statistics about the lookup system."""
        return {
            'total_songs': len(self.songs_by_id),
            'unique_titles': len(self.songs_by_title),
            'unique_artists': len(self.songs_by_artist)
        }