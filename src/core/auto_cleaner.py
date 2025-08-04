"""
Auto Cleaner using HashSet implementation
Removes duplicate songs based on composite keys
"""

from typing import List, Dict, Set, Tuple
from models.song import Song

class AutoCleaner:
    """
    HashSet-based duplicate detection and removal system.
    Uses composite keys for flexible duplicate detection.
    
    Time Complexity:
    - Add song: O(1) average
    - Remove duplicates: O(n) where n is number of songs
    - Find duplicates: O(n)
    
    Space Complexity: O(n) for hash storage
    """
    
    def __init__(self):
        # Track seen songs by composite key
        self.seen_keys: Set[str] = set()
        
        # Different strategies for generating composite keys
        self.key_strategies = {
            'title_artist': self._generate_title_artist_key,
            'title_artist_duration': self._generate_full_key,
            'title_only': self._generate_title_key,
            'strict': self._generate_strict_key
        }
        
        # Default strategy
        self.current_strategy = 'title_artist'
        
        # Statistics
        self.duplicates_found = 0
        self.unique_songs_processed = 0
    
    def set_duplicate_strategy(self, strategy: str) -> bool:
        """
        Set the strategy for detecting duplicates.
        
        Args:
            strategy: Strategy name ('title_artist', 'title_artist_duration', 
                     'title_only', 'strict')
                     
        Returns:
            bool: True if strategy is valid
        """
        if strategy in self.key_strategies:
            self.current_strategy = strategy
            self.clear_cache()
            return True
        return False
    
    def remove_duplicates(self, songs: List[Song]) -> List[Song]:
        """
        Remove duplicate songs from the provided list.
        
        Args:
            songs: List of songs to process
            
        Returns:
            List[Song]: List with duplicates removed
            
        Time Complexity: O(n)
        """
        unique_songs = []
        seen_in_this_batch = set()
        key_generator = self.key_strategies[self.current_strategy]
        
        for song in songs:
            composite_key = key_generator(song)
            
            if composite_key not in seen_in_this_batch:
                seen_in_this_batch.add(composite_key)
                unique_songs.append(song)
                self.unique_songs_processed += 1
            else:
                self.duplicates_found += 1
        
        return unique_songs
    
    def find_duplicates(self, songs: List[Song]) -> List[Tuple[Song, List[Song]]]:
        """
        Find duplicate songs in the provided list.
        
        Args:
            songs: List of songs to analyze
            
        Returns:
            List[Tuple[Song, List[Song]]]: List of (original, duplicates) pairs
            
        Time Complexity: O(n)
        """
        key_to_songs: Dict[str, List[Song]] = {}
        key_generator = self.key_strategies[self.current_strategy]
        
        # Group songs by composite key
        for song in songs:
            composite_key = key_generator(song)
            if composite_key not in key_to_songs:
                key_to_songs[composite_key] = []
            key_to_songs[composite_key].append(song)
        
        # Find groups with more than one song (duplicates)
        duplicate_groups = []
        for key, song_group in key_to_songs.items():
            if len(song_group) > 1:
                # First song is considered original, rest are duplicates
                original = song_group[0]
                duplicates = song_group[1:]
                duplicate_groups.append((original, duplicates))
                self.duplicates_found += len(duplicates)
        
        return duplicate_groups
    
    def get_duplicate_stats(self, songs: List[Song]) -> Dict[str, int]:
        """
        Get statistics about duplicates in the song list.
        
        Args:
            songs: List of songs to analyze
            
        Returns:
            Dict: Statistics about duplicates
        """
        duplicate_groups = self.find_duplicates(songs)
        
        total_duplicates = sum(len(duplicates) for _, duplicates in duplicate_groups)
        unique_songs = len(songs) - total_duplicates
        
        return {
            'total_songs': len(songs),
            'unique_songs': unique_songs,
            'duplicate_songs': total_duplicates,
            'duplicate_groups': len(duplicate_groups),
            'duplicate_percentage': (total_duplicates / len(songs) * 100) if songs else 0
        }
    
    def clean_playlist_duplicates(self, songs: List[Song], 
                                 keep_highest_rated: bool = True) -> List[Song]:
        """
        Remove duplicates with smart selection of which version to keep.
        
        Args:
            songs: List of songs to clean
            keep_highest_rated: If True, keeps the highest-rated version
            
        Returns:
            List[Song]: Cleaned list
        """
        key_to_best_song: Dict[str, Song] = {}
        key_generator = self.key_strategies[self.current_strategy]
        
        for song in songs:
            composite_key = key_generator(song)
            
            if composite_key not in key_to_best_song:
                key_to_best_song[composite_key] = song
            else:
                existing_song = key_to_best_song[composite_key]
                
                if keep_highest_rated:
                    # Keep the song with higher rating, or higher play count as tiebreaker
                    if (song.rating > existing_song.rating or 
                        (song.rating == existing_song.rating and 
                         song.play_count > existing_song.play_count)):
                        key_to_best_song[composite_key] = song
                else:
                    # Keep the first occurrence
                    pass
        
        return list(key_to_best_song.values())
    
    def _generate_title_artist_key(self, song: Song) -> str:
        """Generate composite key from title and artist."""
        return f"{song.title.lower().strip()}_{song.artist.lower().strip()}"
    
    def _generate_full_key(self, song: Song) -> str:
        """Generate composite key from title, artist, and duration."""
        return f"{song.title.lower().strip()}_{song.artist.lower().strip()}_{song.duration}"
    
    def _generate_title_key(self, song: Song) -> str:
        """Generate composite key from title only."""
        return song.title.lower().strip()
    
    def _generate_strict_key(self, song: Song) -> str:
        """Generate strict key including all major attributes."""
        return (f"{song.title.lower().strip()}_{song.artist.lower().strip()}_"
                f"{song.duration}_{song.rating}")
    
    def merge_duplicate_metadata(self, original: Song, duplicates: List[Song]) -> Song:
        """
        Merge metadata from duplicate songs into the original.
        
        Args:
            original: The song to keep
            duplicates: List of duplicate songs
            
        Returns:
            Song: Original song with merged metadata
        """
        # Sum play counts and listen times
        total_play_count = original.play_count
        total_listen_time = original.listen_time
        
        for duplicate in duplicates:
            total_play_count += duplicate.play_count
            total_listen_time += duplicate.listen_time
        
        # Update original with merged data
        original.play_count = total_play_count
        original.listen_time = total_listen_time
        
        # Use highest rating
        highest_rating = max([original.rating] + [d.rating for d in duplicates])
        original.rating = highest_rating
        
        return original
    
    def clear_cache(self) -> None:
        """Clear the internal cache of seen keys."""
        self.seen_keys.clear()
    
    def get_cleaning_stats(self) -> Dict[str, int]:
        """Get statistics about the cleaning process."""
        return {
            'duplicates_found': self.duplicates_found,
            'unique_songs_processed': self.unique_songs_processed,
            'current_strategy': self.current_strategy
        }
    
    def reset_stats(self) -> None:
        """Reset cleaning statistics."""
        self.duplicates_found = 0
        self.unique_songs_processed = 0
    
    def validate_song_uniqueness(self, songs: List[Song]) -> bool:
        """
        Validate that all songs in the list are unique according to current strategy.
        
        Args:
            songs: List of songs to validate
            
        Returns:
            bool: True if all songs are unique
        """
        seen_keys = set()
        key_generator = self.key_strategies[self.current_strategy]
        
        for song in songs:
            composite_key = key_generator(song)
            if composite_key in seen_keys:
                return False
            seen_keys.add(composite_key)
        
        return True
