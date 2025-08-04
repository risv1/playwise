"""
Playlist Sorter implementing multiple sorting algorithms
Sorts playlists based on various criteria with performance comparison
"""

from typing import List, Callable, Any
from enum import Enum
import time
from models.song import Song

class SortAlgorithm(Enum):
    """Available sorting algorithms"""
    MERGE = "merge"
    QUICK = "quick"
    BUILTIN = "builtin"

class SortCriteria(Enum):
    """Available sorting criteria"""
    TITLE = "title"
    ARTIST = "artist"
    DURATION = "duration"
    RATING = "rating"
    DATE_ADDED = "date_added"
    PLAY_COUNT = "play_count"

class PlaylistSorter:
    """
    Implements various sorting algorithms for playlists.
    
    Algorithms and their complexities:
    - Merge Sort: O(n log n) time, O(n) space, stable
    - Quick Sort: O(n log n) average, O(n²) worst, O(log n) space, unstable
    - Built-in Sort: O(n log n) time, O(n) space, stable (Timsort)
    """
    
    def __init__(self):
        self.last_sort_time = 0.0
        self.sort_stats = {
            'merge': {'calls': 0, 'total_time': 0.0},
            'quick': {'calls': 0, 'total_time': 0.0},
            'builtin': {'calls': 0, 'total_time': 0.0}
        }
    
    def sort_by_title(self, songs: List[Song], reverse: bool = False, 
                     algorithm: str = "builtin") -> List[Song]:
        """
        Sort songs by title.
        
        Args:
            songs: List of songs to sort
            reverse: Sort in descending order if True
            algorithm: Sorting algorithm to use
            
        Returns:
            List[Song]: Sorted list of songs
            
        Time Complexity: O(n log n)
        """
        key_func = lambda song: song.title.lower()
        return self._sort_with_algorithm(songs, key_func, reverse, algorithm)
    
    def sort_by_artist(self, songs: List[Song], reverse: bool = False, 
                      algorithm: str = "builtin") -> List[Song]:
        """Sort songs by artist name."""
        key_func = lambda song: song.artist.lower()
        return self._sort_with_algorithm(songs, key_func, reverse, algorithm)
    
    def sort_by_duration(self, songs: List[Song], reverse: bool = False, 
                        algorithm: str = "builtin") -> List[Song]:
        """Sort songs by duration."""
        key_func = lambda song: song.duration
        return self._sort_with_algorithm(songs, key_func, reverse, algorithm)
    
    def sort_by_rating(self, songs: List[Song], reverse: bool = False, 
                      algorithm: str = "builtin") -> List[Song]:
        """Sort songs by rating."""
        key_func = lambda song: song.rating
        return self._sort_with_algorithm(songs, key_func, reverse, algorithm)
    
    def sort_by_date_added(self, songs: List[Song], reverse: bool = False, 
                          algorithm: str = "builtin") -> List[Song]:
        """Sort songs by date added."""
        key_func = lambda song: song.date_added
        return self._sort_with_algorithm(songs, key_func, reverse, algorithm)
    
    def sort_by_play_count(self, songs: List[Song], reverse: bool = False, 
                          algorithm: str = "builtin") -> List[Song]:
        """Sort songs by play count."""
        key_func = lambda song: song.play_count
        return self._sort_with_algorithm(songs, key_func, reverse, algorithm)
    
    def _sort_with_algorithm(self, songs: List[Song], key_func: Callable, 
                           reverse: bool, algorithm: str) -> List[Song]:
        """
        Sort using the specified algorithm.
        
        Args:
            songs: List of songs to sort
            key_func: Function to extract sort key
            reverse: Sort in descending order if True
            algorithm: Algorithm to use
            
        Returns:
            List[Song]: Sorted list
        """
        start_time = time.time()
        
        # Create a copy to avoid modifying original
        songs_copy = songs.copy()
        
        if algorithm == "merge":
            result = self._merge_sort(songs_copy, key_func)
        elif algorithm == "quick":
            result = self._quick_sort(songs_copy, key_func)
        else:  # builtin
            result = sorted(songs_copy, key=key_func)
        
        if reverse:
            result.reverse()
        
        # Track performance
        end_time = time.time()
        sort_time = end_time - start_time
        self.last_sort_time = sort_time
        
        if algorithm in self.sort_stats:
            self.sort_stats[algorithm]['calls'] += 1
            self.sort_stats[algorithm]['total_time'] += sort_time
        
        return result
    
    def _merge_sort(self, songs: List[Song], key_func: Callable) -> List[Song]:
        """
        Merge sort implementation.
        
        Time Complexity: O(n log n)
        Space Complexity: O(n)
        Stability: Stable
        """
        if len(songs) <= 1:
            return songs
        
        mid = len(songs) // 2
        left_half = songs[:mid]
        right_half = songs[mid:]
        
        left_sorted = self._merge_sort(left_half, key_func)
        right_sorted = self._merge_sort(right_half, key_func)
        
        return self._merge(left_sorted, right_sorted, key_func)
    
    def _merge(self, left: List[Song], right: List[Song], key_func: Callable) -> List[Song]:
        """Merge two sorted lists."""
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Add remaining elements
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    def _quick_sort(self, songs: List[Song], key_func: Callable) -> List[Song]:
        """
        Quick sort implementation.
        
        Time Complexity: O(n log n) average, O(n²) worst
        Space Complexity: O(log n) average
        Stability: Unstable
        """
        if len(songs) <= 1:
            return songs
        
        pivot = songs[len(songs) // 2]
        pivot_key = key_func(pivot)
        
        left = [x for x in songs if key_func(x) < pivot_key]
        middle = [x for x in songs if key_func(x) == pivot_key]
        right = [x for x in songs if key_func(x) > pivot_key]
        
        return (self._quick_sort(left, key_func) + 
                middle + 
                self._quick_sort(right, key_func))
    
    def sort_by_multiple_criteria(self, songs: List[Song], 
                                 criteria_list: List[tuple]) -> List[Song]:
        """
        Sort by multiple criteria in order of priority.
        
        Args:
            songs: List of songs to sort
            criteria_list: List of (criteria, reverse) tuples
            
        Returns:
            List[Song]: Sorted list
            
        Example:
            sorter.sort_by_multiple_criteria(songs, [
                ('rating', True),   # Primary: rating descending
                ('title', False)    # Secondary: title ascending
            ])
        """
        if not criteria_list:
            return songs.copy()
        
        # Create key function for multiple criteria
        def multi_key(song):
            keys = []
            for criteria, reverse in criteria_list:
                if criteria == 'title':
                    key = song.title.lower()
                elif criteria == 'artist':
                    key = song.artist.lower()
                elif criteria == 'duration':
                    key = song.duration
                elif criteria == 'rating':
                    key = song.rating
                elif criteria == 'date_added':
                    key = song.date_added
                elif criteria == 'play_count':
                    key = song.play_count
                else:
                    key = 0
                
                # Negate for reverse order
                if reverse:
                    if isinstance(key, str):
                        # For strings, we'll handle reverse in the main sort
                        keys.append((key, True))
                    else:
                        keys.append(-key)
                else:
                    if isinstance(key, str):
                        keys.append((key, False))
                    else:
                        keys.append(key)
            
            return keys
        
        return sorted(songs, key=multi_key)
    
    def benchmark_algorithms(self, songs: List[Song], 
                           criteria: str = "duration") -> dict:
        """
        Benchmark all sorting algorithms on the given dataset.
        
        Args:
            songs: List of songs to sort
            criteria: Sorting criteria to use
            
        Returns:
            dict: Performance results for each algorithm
        """
        key_func = self._get_key_function(criteria)
        results = {}
        
        for algorithm in ["merge", "quick", "builtin"]:
            start_time = time.time()
            
            # Sort multiple times for more accurate measurement
            for _ in range(5):
                self._sort_with_algorithm(songs, key_func, False, algorithm)
            
            avg_time = (time.time() - start_time) / 5
            results[algorithm] = {
                'avg_time': avg_time,
                'time_per_item': avg_time / len(songs) if songs else 0
            }
        
        return results
    
    def _get_key_function(self, criteria: str) -> Callable:
        """Get key function for the specified criteria."""
        if criteria == "title":
            return lambda song: song.title.lower()
        elif criteria == "artist":
            return lambda song: song.artist.lower()
        elif criteria == "duration":
            return lambda song: song.duration
        elif criteria == "rating":
            return lambda song: song.rating
        elif criteria == "date_added":
            return lambda song: song.date_added
        elif criteria == "play_count":
            return lambda song: song.play_count
        else:
            return lambda song: song.title.lower()
    
    def get_performance_stats(self) -> dict:
        """Get performance statistics for all algorithms."""
        stats = {}
        for algorithm, data in self.sort_stats.items():
            if data['calls'] > 0:
                stats[algorithm] = {
                    'total_calls': data['calls'],
                    'total_time': data['total_time'],
                    'average_time': data['total_time'] / data['calls']
                }
            else:
                stats[algorithm] = {
                    'total_calls': 0,
                    'total_time': 0.0,
                    'average_time': 0.0
                }
        
        return stats
    
    def reset_stats(self) -> None:
        """Reset performance statistics."""
        for algorithm in self.sort_stats:
            self.sort_stats[algorithm] = {'calls': 0, 'total_time': 0.0}
    
    def get_last_sort_time(self) -> float:
        """Get the time taken for the last sort operation."""
        return self.last_sort_time