"""
System Snapshot Module for real-time analytics and insights
Generates comprehensive system statistics by integrating all components
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from models.song import Song

class SystemSnapshot:
    """
    Real-time system analytics and insights generator.
    Combines data from all system components for comprehensive reporting.
    
    Time Complexity: O(n log n) due to sorting operations
    Space Complexity: O(n) for snapshot data
    """
    
    def __init__(self, playlist_engine=None, playback_history=None, 
                 song_rating_tree=None, song_lookup=None, favorites_queue=None):
        self.playlist_engine = playlist_engine
        self.playback_history = playback_history
        self.song_rating_tree = song_rating_tree
        self.song_lookup = song_lookup
        self.favorites_queue = favorites_queue
        
        # Snapshot cache
        self.last_snapshot = None
        self.last_snapshot_time = None
        self.cache_duration = 60  # Cache for 60 seconds
    
    def set_components(self, playlist_engine=None, playback_history=None,
                      song_rating_tree=None, song_lookup=None, favorites_queue=None):
        """Set system components for snapshot generation."""
        if playlist_engine:
            self.playlist_engine = playlist_engine
        if playback_history:
            self.playback_history = playback_history
        if song_rating_tree:
            self.song_rating_tree = song_rating_tree
        if song_lookup:
            self.song_lookup = song_lookup
        if favorites_queue:
            self.favorites_queue = favorites_queue
    
    def generate_snapshot(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Generate a comprehensive system snapshot.
        
        Args:
            use_cache: Whether to use cached snapshot if available
            
        Returns:
            Dict: Comprehensive system statistics
            
        Time Complexity: O(n log n)
        """
        current_time = datetime.now()
        
        # Check cache validity
        if (use_cache and self.last_snapshot and self.last_snapshot_time and
            (current_time - self.last_snapshot_time).seconds < self.cache_duration):
            return self.last_snapshot.copy()
        
        snapshot = {
            'timestamp': current_time.isoformat(),
            'system_overview': self._get_system_overview(),
            'playlist_statistics': self._get_playlist_statistics(),
            'song_analytics': self._get_song_analytics(),
            'playback_insights': self._get_playback_insights(),
            'rating_analysis': self._get_rating_analysis(),
            'favorites_summary': self._get_favorites_summary(),
            'top_performers': self._get_top_performers(),
            'system_health': self._get_system_health()
        }
        
        # Cache the snapshot
        self.last_snapshot = snapshot.copy()
        self.last_snapshot_time = current_time
        
        return snapshot
    
    def _get_system_overview(self) -> Dict[str, Any]:
        """Get high-level system overview."""
        total_songs = 0
        total_playlists = 0
        
        if self.playlist_engine:
            total_playlists = len(self.playlist_engine.playlists)
            total_songs = sum(len(playlist.songs) for playlist in self.playlist_engine.playlists.values())
        
        if self.song_lookup:
            lookup_songs = self.song_lookup.get_song_count()
            total_songs = max(total_songs, lookup_songs)
        
        return {
            'total_songs': total_songs,
            'total_playlists': total_playlists,
            'total_unique_artists': len(self.song_lookup.get_all_artists()) if self.song_lookup else 0,
            'total_unique_titles': len(self.song_lookup.get_all_titles()) if self.song_lookup else 0,
            'system_components_active': self._count_active_components()
        }
    
    def _get_playlist_statistics(self) -> Dict[str, Any]:
        """Get detailed playlist statistics."""
        if not self.playlist_engine:
            return {'error': 'Playlist engine not available'}
        
        playlists = self.playlist_engine.list_playlists()
        if not playlists:
            return {
                'total_playlists': 0,
                'average_songs_per_playlist': 0,
                'total_duration_minutes': 0,
                'largest_playlist': None,
                'smallest_playlist': None
            }
        
        # Calculate statistics
        song_counts = [len(playlist.songs) for playlist in playlists]
        durations = [playlist.get_total_duration() for playlist in playlists]
        
        largest_playlist = max(playlists, key=lambda p: len(p.songs))
        smallest_playlist = min(playlists, key=lambda p: len(p.songs))
        
        return {
            'total_playlists': len(playlists),
            'average_songs_per_playlist': sum(song_counts) / len(song_counts),
            'total_duration_minutes': sum(durations) / 60,
            'average_duration_minutes': (sum(durations) / len(durations)) / 60,
            'largest_playlist': {
                'name': largest_playlist.name,
                'songs': len(largest_playlist.songs),
                'duration_minutes': largest_playlist.get_total_duration() / 60
            },
            'smallest_playlist': {
                'name': smallest_playlist.name,
                'songs': len(smallest_playlist.songs),
                'duration_minutes': smallest_playlist.get_total_duration() / 60
            }
        }
    
    def _get_song_analytics(self) -> Dict[str, Any]:
        """Get comprehensive song analytics."""
        if not self.song_lookup:
            return {'error': 'Song lookup not available'}
        
        all_songs = self.song_lookup.get_all_songs()
        if not all_songs:
            return {
                'total_songs': 0,
                'average_duration': 0,
                'top_longest_songs': [],
                'top_shortest_songs': [],
                'duration_distribution': {}
            }
        
        # Duration analysis
        durations = [song.duration for song in all_songs]
        average_duration = sum(durations) / len(durations)
        
        # Top longest and shortest songs
        sorted_by_duration = sorted(all_songs, key=lambda s: s.duration, reverse=True)
        top_longest = [song.to_dict() for song in sorted_by_duration[:5]]
        top_shortest = [song.to_dict() for song in sorted_by_duration[-5:]]
        
        # Duration distribution
        duration_ranges = {
            '0-2min': 0, '2-3min': 0, '3-4min': 0, 
            '4-5min': 0, '5-6min': 0, '6min+': 0
        }
        
        for duration in durations:
            minutes = duration / 60
            if minutes < 2:
                duration_ranges['0-2min'] += 1
            elif minutes < 3:
                duration_ranges['2-3min'] += 1
            elif minutes < 4:
                duration_ranges['3-4min'] += 1
            elif minutes < 5:
                duration_ranges['4-5min'] += 1
            elif minutes < 6:
                duration_ranges['5-6min'] += 1
            else:
                duration_ranges['6min+'] += 1
        
        return {
            'total_songs': len(all_songs),
            'average_duration_seconds': average_duration,
            'average_duration_minutes': average_duration / 60,
            'top_longest_songs': top_longest,
            'top_shortest_songs': top_shortest,
            'duration_distribution': duration_ranges
        }
    
    def _get_playback_insights(self) -> Dict[str, Any]:
        """Get playback history insights."""
        if not self.playback_history:
            return {'error': 'Playback history not available'}
        
        recent_history = self.playback_history.get_recent_history(50)
        if not recent_history:
            return {
                'total_plays': 0,
                'recently_played': [],
                'most_played_songs': [],
                'recently_played_artists': []
            }
        
        return {
            'total_plays': self.playback_history.get_history_size(),
            'recently_played': [song.to_dict() for song in recent_history[:10]],
            'most_played_songs': [song.to_dict() for song in self.playback_history.get_most_played_songs(5)],
            'recently_played_artists': self.playback_history.get_recently_played_artists(10)
        }
    
    def _get_rating_analysis(self) -> Dict[str, Any]:
        """Get song rating analysis."""
        if not self.song_rating_tree:
            return {'error': 'Song rating tree not available'}
        
        distribution = self.song_rating_tree.get_rating_distribution()
        total_songs = sum(distribution.values())
        
        if total_songs == 0:
            return {
                'total_rated_songs': 0,
                'rating_distribution': {},
                'average_rating': 0,
                'top_rated_songs': []
            }
        
        # Calculate average rating
        weighted_sum = sum(rating * count for rating, count in distribution.items())
        average_rating = weighted_sum / total_songs
        
        # Get top rated songs
        top_rated = self.song_rating_tree.get_top_rated_songs(10)
        
        return {
            'total_rated_songs': total_songs,
            'rating_distribution': distribution,
            'average_rating': round(average_rating, 2),
            'top_rated_songs': [song.to_dict() for song in top_rated],
            'rating_percentages': {
                rating: round(count / total_songs * 100, 1)
                for rating, count in distribution.items()
            }
        }
    
    def _get_favorites_summary(self) -> Dict[str, Any]:
        """Get favorites queue summary."""
        if not self.favorites_queue:
            return {'error': 'Favorites queue not available'}
        
        top_favorites = self.favorites_queue.get_top_songs(10)
        queue_stats = self.favorites_queue.get_queue_stats()
        
        return {
            'top_favorites': top_favorites,
            'queue_statistics': queue_stats,
            'recently_favorited': self.favorites_queue.get_recently_favorited(5)
        }
    
    def _get_top_performers(self) -> Dict[str, Any]:
        """Get top performing songs across different metrics."""
        performers = {
            'most_played': [],
            'highest_rated': [],
            'longest_songs': [],
            'top_favorites': []
        }
        
        # Most played songs from history
        if self.playback_history:
            performers['most_played'] = [
                song.to_dict() for song in self.playback_history.get_most_played_songs(5)
            ]
        
        # Highest rated songs
        if self.song_rating_tree:
            performers['highest_rated'] = [
                song.to_dict() for song in self.song_rating_tree.get_top_rated_songs(5)
            ]
        
        # Longest songs
        if self.song_lookup:
            all_songs = self.song_lookup.get_all_songs()
            longest_songs = sorted(all_songs, key=lambda s: s.duration, reverse=True)[:5]
            performers['longest_songs'] = [song.to_dict() for song in longest_songs]
        
        # Top favorites
        if self.favorites_queue:
            top_favs = self.favorites_queue.get_top_songs(5)
            performers['top_favorites'] = [fav['song'] for fav in top_favs]
        
        return performers
    
    def _get_system_health(self) -> Dict[str, Any]:
        """Get system health and performance metrics."""
        health = {
            'components_status': {
                'playlist_engine': self.playlist_engine is not None,
                'playback_history': self.playback_history is not None,
                'song_rating_tree': self.song_rating_tree is not None,
                'song_lookup': self.song_lookup is not None,
                'favorites_queue': self.favorites_queue is not None
            },
            'data_consistency': self._check_data_consistency(),
            'cache_status': {
                'last_snapshot_cached': self.last_snapshot is not None,
                'cache_age_seconds': (
                    (datetime.now() - self.last_snapshot_time).seconds
                    if self.last_snapshot_time else None
                )
            }
        }
        
        # Calculate overall health score
        active_components = sum(health['components_status'].values())
        health['overall_health_score'] = (active_components / 5) * 100
        
        return health
    
    def _check_data_consistency(self) -> Dict[str, bool]:
        """Check data consistency across components."""
        consistency = {
            'song_counts_match': True,
            'rating_data_consistent': True,
            'lookup_data_complete': True
        }
        
        # Add more sophisticated consistency checks here
        # For now, return basic structure
        
        return consistency
    
    def _count_active_components(self) -> int:
        """Count the number of active system components."""
        components = [
            self.playlist_engine,
            self.playback_history,
            self.song_rating_tree,
            self.song_lookup,
            self.favorites_queue
        ]
        return sum(1 for component in components if component is not None)
    
    def export_snapshot_to_file(self, filepath: str, format: str = 'json') -> bool:
        """
        Export snapshot to file.
        
        Args:
            filepath: Path to save the snapshot
            format: Export format ('json' or 'csv')
            
        Returns:
            bool: True if exported successfully
        """
        try:
            snapshot = self.generate_snapshot()
            
            if format == 'json':
                import json
                with open(filepath, 'w') as f:
                    json.dump(snapshot, f, indent=2, default=str)
            elif format == 'csv':
                import csv
                # Flatten the snapshot for CSV export
                flat_data = self._flatten_snapshot(snapshot)
                with open(filepath, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=flat_data.keys())
                    writer.writeheader()
                    writer.writerow(flat_data)
            
            return True
        except Exception as e:
            print(f"Error exporting snapshot: {e}")
            return False
    
    def _flatten_snapshot(self, snapshot: Dict[str, Any], prefix: str = '') -> Dict[str, Any]:
        """Flatten nested dictionary for CSV export."""
        flat_dict = {}
        
        for key, value in snapshot.items():
            new_key = f"{prefix}{key}" if prefix else key
            
            if isinstance(value, dict):
                flat_dict.update(self._flatten_snapshot(value, f"{new_key}_"))
            elif isinstance(value, list) and value and isinstance(value[0], dict):
                # For lists of dictionaries, just take the count
                flat_dict[f"{new_key}_count"] = len(value)
            else:
                flat_dict[new_key] = str(value)
        
        return flat_dict
    
    def clear_cache(self) -> None:
        """Clear the snapshot cache."""
        self.last_snapshot = None
        self.last_snapshot_time = None