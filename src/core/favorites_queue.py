"""
Favorites Queue using Min-Heap implementation
Maintains a sorted queue of favorite songs by listen time
"""

import heapq
from typing import List, Dict, Optional
from models.song import Song

class FavoriteItem:
    """Wrapper class for heap items to enable max-heap behavior with min-heap."""
    
    def __init__(self, song: Song, priority_value: float):
        self.song = song
        # Negative value for max-heap behavior using min-heap
        self.priority = -priority_value
        self.listen_time = song.listen_time
        self.play_count = song.play_count
    
    def __lt__(self, other):
        # Primary sort by priority (listen time), secondary by play count
        if self.priority != other.priority:
            return self.priority < other.priority
        return -self.play_count < -other.play_count
    
    def __eq__(self, other):
        return self.song.id == other.song.id if hasattr(other, 'song') else False

class FavoritesQueue:
    """
    Binary heap-based favorites queue for maintaining top songs by listen time.
    Uses negative values to achieve max-heap behavior with Python's min-heap.
    
    Time Complexity:
    - Add song: O(log n)
    - Update listen time: O(n) due to heap rebuild
    - Get top songs: O(k log n) where k is number requested
    
    Space Complexity: O(n) for heap storage
    """
    
    def __init__(self, max_size: int = 1000):
        self.heap: List[FavoriteItem] = []
        self.song_index: Dict[str, int] = {}  # song_id -> heap_index
        self.max_size = max_size
        
        # Metrics
        self.total_listen_time = 0
        self.total_songs_added = 0
    
    def add_song(self, song: Song, listen_time: Optional[int] = None) -> bool:
        """
        Add a song to the favorites queue.
        
        Args:
            song: Song object to add
            listen_time: Optional listen time (uses song.listen_time if None)
            
        Returns:
            bool: True if added successfully
            
        Time Complexity: O(log n)
        """
        if song.id in self.song_index:
            # Update existing song
            return self.update_listen_time(song.id, listen_time or song.listen_time)
        
        priority_value = listen_time if listen_time is not None else song.listen_time
        if listen_time is not None:
            song.listen_time = listen_time
        
        favorite_item = FavoriteItem(song, priority_value)
        
        # If queue is full, check if new song should replace lowest priority
        if len(self.heap) >= self.max_size:
            if priority_value > -self.heap[0].priority:
                # Remove lowest priority item
                removed_item = heapq.heappop(self.heap)
                if removed_item.song.id in self.song_index:
                    del self.song_index[removed_item.song.id]
            else:
                return False  # New song doesn't qualify for favorites
        
        heapq.heappush(self.heap, favorite_item)
        self.song_index[song.id] = len(self.heap) - 1
        self.total_songs_added += 1
        self.total_listen_time += priority_value
        
        return True
    
    def update_listen_time(self, song_id: str, new_time: int) -> bool:
        """
        Update the listen time for a specific song.
        
        Args:
            song_id: ID of song to update
            new_time: New listen time value
            
        Returns:
            bool: True if updated successfully
            
        Time Complexity: O(n) due to heap rebuild
        """
        # Find and update the song
        updated = False
        for item in self.heap:
            if item.song.id == song_id:
                old_time = item.listen_time
                item.song.listen_time = new_time
                item.listen_time = new_time
                item.priority = -new_time
                self.total_listen_time += (new_time - old_time)
                updated = True
                break
        
        if updated:
            # Rebuild heap to maintain heap property
            heapq.heapify(self.heap)
            self._rebuild_index()
            return True
        
        return False
    
    def get_top_songs(self, count: int) -> List[Dict]:
        """
        Get the top favorite songs based on listen time.
        
        Args:
            count: Number of top songs to retrieve
            
        Returns:
            List[Dict]: Top songs with metadata
            
        Time Complexity: O(k log n) where k is count
        """
        if not self.heap:
            return []
        
        # Create a copy of heap for extraction without modifying original
        heap_copy = self.heap.copy()
        top_songs = []
        
        for _ in range(min(count, len(heap_copy))):
            if heap_copy:
                item = heapq.heappop(heap_copy)
                top_songs.append({
                    'song': item.song.to_dict(),
                    'listen_time': item.listen_time,
                    'play_count': item.play_count,
                    'priority_score': -item.priority
                })
        
        return top_songs
    
    def get_song_position(self, song_id: str) -> Optional[int]:
        """
        Get the position of a song in the favorites ranking.
        
        Args:
            song_id: ID of song to find
            
        Returns:
            Optional[int]: Position (1-based) or None if not found
        """
        if song_id not in self.song_index:
            return None
        
        # Sort all items by priority to get position
        sorted_items = sorted(self.heap, key=lambda x: x.priority)
        
        for i, item in enumerate(sorted_items):
            if item.song.id == song_id:
                return i + 1  # 1-based position
        
        return None
    
    def remove_song(self, song_id: str) -> bool:
        """
        Remove a song from the favorites queue.
        
        Args:
            song_id: ID of song to remove
            
        Returns:
            bool: True if removed successfully
        """
        if song_id not in self.song_index:
            return False
        
        # Find and remove the song
        self.heap = [item for item in self.heap if item.song.id != song_id]
        heapq.heapify(self.heap)
        
        # Remove from index
        del self.song_index[song_id]
        
        # Rebuild index
        self._rebuild_index()
        
        return True
    
    def get_favorites_by_artist(self, artist: str, limit: int = 10) -> List[Dict]:
        """Get favorite songs by a specific artist."""
        artist_songs = []
        artist_lower = artist.lower()
        
        for item in self.heap:
            if item.song.artist.lower() == artist_lower:
                artist_songs.append({
                    'song': item.song.to_dict(),
                    'listen_time': item.listen_time,
                    'play_count': item.play_count,
                    'priority_score': -item.priority
                })
        
        # Sort by priority and return top items
        artist_songs.sort(key=lambda x: x['priority_score'], reverse=True)
        return artist_songs[:limit]
    
    def get_recently_favorited(self, limit: int = 10) -> List[Dict]:
        """Get recently added favorite songs."""
        # Sort by date_added and return most recent
        recent_items = sorted(
            self.heap,
            key=lambda x: x.song.date_added,
            reverse=True
        )
        
        result = []
        for item in recent_items[:limit]:
            result.append({
                'song': item.song.to_dict(),
                'listen_time': item.listen_time,
                'play_count': item.play_count,
                'priority_score': -item.priority
            })
        
        return result
    
    def get_queue_stats(self) -> Dict:
        """Get statistics about the favorites queue."""
        if not self.heap:
            return {
                'total_songs': 0,
                'average_listen_time': 0,
                'total_listen_time': 0,
                'top_listen_time': 0,
                'capacity_used': 0
            }
        
        listen_times = [-item.priority for item in self.heap]
        
        return {
            'total_songs': len(self.heap),
            'average_listen_time': sum(listen_times) / len(listen_times),
            'total_listen_time': sum(listen_times),
            'top_listen_time': max(listen_times),
            'lowest_listen_time': min(listen_times),
            'capacity_used': len(self.heap) / self.max_size * 100,
            'max_capacity': self.max_size
        }
    
    def clear_queue(self) -> None:
        """Clear all songs from the favorites queue."""
        self.heap.clear()
        self.song_index.clear()
        self.total_listen_time = 0
        self.total_songs_added = 0
    
    def is_empty(self) -> bool:
        """Check if the favorites queue is empty."""
        return len(self.heap) == 0
    
    def is_full(self) -> bool:
        """Check if the favorites queue is at capacity."""
        return len(self.heap) >= self.max_size
    
    def _rebuild_index(self) -> None:
        """Rebuild the song index after heap modifications."""
        self.song_index.clear()
        for i, item in enumerate(self.heap):
            self.song_index[item.song.id] = i
    
    def bulk_update_from_playback_history(self, songs_with_times: List[tuple]) -> int:
        """
        Bulk update favorites from playback history.
        
        Args:
            songs_with_times: List of (song, listen_time) tuples
            
        Returns:
            int: Number of songs successfully updated
        """
        updated_count = 0
        
        for song, listen_time in songs_with_times:
            if self.add_song(song, listen_time):
                updated_count += 1
        
        return updated_count
