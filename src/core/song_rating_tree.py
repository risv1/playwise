"""
Song Rating Tree using Binary Search Tree implementation
Organizes songs by rating for fast rating-based queries
"""

from typing import List, Optional, Dict
from models.song import Song

class RatingNode:
    """Node for BST storing songs grouped by rating"""
    
    def __init__(self, rating: int):
        self.rating = rating
        self.songs: List[Song] = []  # Multiple songs can have same rating
        self.left: Optional['RatingNode'] = None
        self.right: Optional['RatingNode'] = None

class SongRatingTree:
    """
    Binary Search Tree for organizing songs by rating.
    Each node contains all songs with a specific rating.
    
    Time Complexity:
    - Insert: O(log n) average, O(n) worst case
    - Search: O(log n) average, O(n) worst case  
    - Delete: O(log n) average, O(n) worst case
    - Range query: O(log n + k) where k is result size
    
    Space Complexity: O(n) where n is number of unique ratings (max 6: 0-5)
    """
    
    def __init__(self):
        self.root: Optional[RatingNode] = None
        self.total_songs = 0
    
    def insert_song(self, song: Song, rating: Optional[int] = None) -> bool:
        """
        Insert a song with its rating into the tree.
        
        Args:
            song: Song object to insert
            rating: Rating to use (uses song.rating if None)
            
        Returns:
            bool: True if inserted successfully
            
        Time Complexity: O(log n) average
        """
        target_rating = rating if rating is not None else song.rating
        target_rating = max(0, min(5, target_rating))  # Ensure valid range
        
        if self.root is None:
            self.root = RatingNode(target_rating)
            self.root.songs.append(song)
            self.total_songs += 1
            return True
        
        return self._insert_recursive(self.root, song, target_rating)
    
    def _insert_recursive(self, node: RatingNode, song: Song, rating: int) -> bool:
        """Recursive helper for insertion."""
        if rating == node.rating:
            # Song with this rating already exists in this node
            if song not in node.songs:
                node.songs.append(song)
                self.total_songs += 1
                return True
            return False  # Song already exists
        elif rating < node.rating:
            if node.left is None:
                node.left = RatingNode(rating)
                node.left.songs.append(song)
                self.total_songs += 1
                return True
            return self._insert_recursive(node.left, song, rating)
        else:
            if node.right is None:
                node.right = RatingNode(rating)
                node.right.songs.append(song)
                self.total_songs += 1
                return True
            return self._insert_recursive(node.right, song, rating)
    
    def search_by_rating(self, rating: int) -> List[Song]:
        """
        Search for all songs with a specific rating.
        
        Args:
            rating: Rating to search for (0-5)
            
        Returns:
            List[Song]: Songs with the specified rating
            
        Time Complexity: O(log n)
        """
        rating = max(0, min(5, rating))  # Ensure valid range
        node = self._find_node(self.root, rating)
        return node.songs.copy() if node else []
    
    def _find_node(self, node: Optional[RatingNode], rating: int) -> Optional[RatingNode]:
        """Find node with specific rating."""
        if node is None or node.rating == rating:
            return node
        
        if rating < node.rating:
            return self._find_node(node.left, rating)
        else:
            return self._find_node(node.right, rating)
    
    def delete_song(self, song_id: str) -> bool:
        """
        Delete a song from the tree by its ID.
        
        Args:
            song_id: ID of song to delete
            
        Returns:
            bool: True if deleted successfully
            
        Time Complexity: O(log n * m) where m is avg songs per rating
        """
        return self._delete_song_recursive(self.root, song_id)
    
    def _delete_song_recursive(self, node: Optional[RatingNode], song_id: str) -> bool:
        """Recursive helper for song deletion."""
        if node is None:
            return False
        
        # Check current node
        for i, song in enumerate(node.songs):
            if song.id == song_id:
                node.songs.pop(i)
                self.total_songs -= 1
                
                # If node becomes empty, we could remove it (complex BST deletion)
                # For now, keep empty nodes for simplicity
                return True
        
        # Search in subtrees
        found_left = self._delete_song_recursive(node.left, song_id)
        if found_left:
            return True
        
        return self._delete_song_recursive(node.right, song_id)
    
    def get_songs_by_rating_range(self, min_rating: int = 0, max_rating: int = 5) -> List[Song]:
        """
        Get all songs within a rating range.
        
        Args:
            min_rating: Minimum rating (inclusive)
            max_rating: Maximum rating (inclusive)
            
        Returns:
            List[Song]: Songs within the rating range
            
        Time Complexity: O(log n + k) where k is result size
        """
        min_rating = max(0, min(5, min_rating))
        max_rating = max(0, min(5, max_rating))
        
        if min_rating > max_rating:
            min_rating, max_rating = max_rating, min_rating
        
        result = []
        self._range_search(self.root, min_rating, max_rating, result)
        return result
    
    def _range_search(self, node: Optional[RatingNode], min_rating: int, 
                     max_rating: int, result: List[Song]) -> None:
        """Recursive helper for range search."""
        if node is None:
            return
        
        # If current rating is in range, add all songs
        if min_rating <= node.rating <= max_rating:
            result.extend(node.songs)
        
        # Search left subtree if needed
        if min_rating < node.rating:
            self._range_search(node.left, min_rating, max_rating, result)
        
        # Search right subtree if needed
        if max_rating > node.rating:
            self._range_search(node.right, min_rating, max_rating, result)
    
    def get_rating_distribution(self) -> Dict[int, int]:
        """
        Get distribution of songs by rating.
        
        Returns:
            Dict[int, int]: Rating -> count mapping
            
        Time Complexity: O(n)
        """
        distribution = {}
        self._collect_distribution(self.root, distribution)
        return distribution
    
    def _collect_distribution(self, node: Optional[RatingNode], 
                            distribution: Dict[int, int]) -> None:
        """Recursive helper for collecting rating distribution."""
        if node is None:
            return
        
        if node.songs:  # Only count non-empty nodes
            distribution[node.rating] = len(node.songs)
        
        self._collect_distribution(node.left, distribution)
        self._collect_distribution(node.right, distribution)
    
    def get_all_songs(self) -> List[Song]:
        """Get all songs from the tree."""
        result = []
        self._collect_all_songs(self.root, result)
        return result
    
    def _collect_all_songs(self, node: Optional[RatingNode], result: List[Song]) -> None:
        """Recursive helper for collecting all songs."""
        if node is None:
            return
        
        result.extend(node.songs)
        self._collect_all_songs(node.left, result)
        self._collect_all_songs(node.right, result)
    
    def get_top_rated_songs(self, limit: int = 10) -> List[Song]:
        """Get top rated songs (5-star first, then 4-star, etc.)."""
        result = []
        for rating in range(5, -1, -1):  # 5 down to 0
            songs = self.search_by_rating(rating)
            result.extend(songs)
            if len(result) >= limit:
                break
        
        return result[:limit]
    
    def is_empty(self) -> bool:
        """Check if tree is empty."""
        return self.root is None
    
    def get_song_count(self) -> int:
        """Get total number of songs in tree."""
        return self.total_songs