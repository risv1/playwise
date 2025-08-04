"""
Main PlayWise Engine class that integrates all components
"""

from typing import Dict, List, Optional, Any
from core.playlist_engine import PlaylistEngine
from core.playback_history import PlaybackHistory
from core.song_rating_tree import SongRatingTree
from core.song_lookup import SongLookup
from core.playlist_sorter import PlaylistSorter
from core.auto_cleaner import AutoCleaner
from core.favorites_queue import FavoritesQueue
from core.system_snapshot import SystemSnapshot
from models.song import Song
from models.playlist import Playlist

class PlayWiseEngine:
    """
    Main PlayWise Engine that orchestrates all components.
    Provides a unified interface for the music playlist management system.
    """
    
    def __init__(self):
        # Initialize all core components
        self.playlist_engine = PlaylistEngine()
        self.playback_history = PlaybackHistory()
        self.song_rating_tree = SongRatingTree()
        self.song_lookup = SongLookup()
        self.playlist_sorter = PlaylistSorter()
        self.auto_cleaner = AutoCleaner()
        self.favorites_queue = FavoritesQueue()
        
        # Initialize system snapshot with all components
        self.system_snapshot = SystemSnapshot(
            playlist_engine=self.playlist_engine,
            playback_history=self.playback_history,
            song_rating_tree=self.song_rating_tree,
            song_lookup=self.song_lookup,
            favorites_queue=self.favorites_queue
        )
        
        # Engine metadata
        self.version = "1.0.0"
        self.initialized = True
    
    def create_song(self, title: str, artist: str, duration: int, rating: int = 0) -> Song:
        """
        Create a new song and add it to the lookup system.
        
        Args:
            title: Song title
            artist: Artist name
            duration: Duration in seconds
            rating: Song rating (0-5)
            
        Returns:
            Song: Created song object
        """
        song = Song(title, artist, duration, rating)
        
        # Add to lookup system
        self.song_lookup.add_song(song)
        
        # Add to rating tree
        self.song_rating_tree.insert_song(song)
        
        return song
    
    def create_playlist(self, name: str, description: str = "") -> str:
        """Create a new playlist."""
        return self.playlist_engine.create_playlist(name, description)
    
    def add_song_to_playlist(self, song_id: str, playlist_id: Optional[str] = None, 
                           position: int = -1) -> bool:
        """Add a song to a playlist."""
        song = self.song_lookup.get_song(song_id)
        if not song:
            return False
        
        return self.playlist_engine.add_song(song, position, playlist_id)
    
    def play_song(self, song_id: str, listen_duration: Optional[int] = None) -> bool:
        """
        Play a song and update all relevant systems.
        
        Args:
            song_id: ID of song to play
            listen_duration: How long the song was listened to (optional)
            
        Returns:
            bool: True if play was recorded successfully
        """
        song = self.song_lookup.get_song(song_id)
        if not song:
            return False
        
        # Add to playback history
        self.playback_history.add_to_history(song)
        
        # Update listen time if provided
        if listen_duration:
            song.add_listen_time(listen_duration)
        
        # Add/update in favorites queue
        self.favorites_queue.add_song(song)
        
        return True
    
    def rate_song(self, song_id: str, rating: int) -> bool:
        """
        Rate a song and update the rating tree.
        
        Args:
            song_id: ID of song to rate
            rating: New rating (0-5)
            
        Returns:
            bool: True if rating was updated successfully
        """
        song = self.song_lookup.get_song(song_id)
        if not song:
            return False
        
        # Update song rating
        old_rating = song.rating
        song.update_rating(rating)
        
        # Update song lookup (handles key changes)
        self.song_lookup.update_song(song)
        
        # Update rating tree (remove old, add new)
        if old_rating != rating:
            self.song_rating_tree.delete_song(song_id)
            self.song_rating_tree.insert_song(song)
        
        return True
    
    def search_songs(self, query: str, search_type: str = "all") -> List[Song]:
        """
        Search for songs by various criteria.
        
        Args:
            query: Search query
            search_type: Type of search ("title", "artist", "all")
            
        Returns:
            List[Song]: Matching songs
        """
        if search_type == "title":
            return self.song_lookup.fuzzy_search_title(query)
        elif search_type == "artist":
            return self.song_lookup.fuzzy_search_artist(query)
        else:  # "all"
            title_results = self.song_lookup.fuzzy_search_title(query)
            artist_results = self.song_lookup.fuzzy_search_artist(query)
            
            # Combine results and remove duplicates
            all_results = title_results + artist_results
            return list(set(all_results))
    
    def get_songs_by_rating(self, min_rating: int = 0, max_rating: int = 5) -> List[Song]:
        """Get songs within a rating range."""
        return self.song_rating_tree.get_songs_by_rating_range(min_rating, max_rating)
    
    def sort_playlist(self, criteria: str, reverse: bool = False, 
                     algorithm: str = "builtin", playlist_id: Optional[str] = None) -> bool:
        """
        Sort a playlist by the specified criteria.
        
        Args:
            criteria: Sort criteria ("title", "artist", "duration", "rating", etc.)
            reverse: Sort in descending order if True
            algorithm: Sorting algorithm to use
            playlist_id: ID of playlist to sort (current if None)
            
        Returns:
            bool: True if sorted successfully
        """
        songs = self.playlist_engine.get_songs(playlist_id)
        if not songs:
            return False
        
        # Sort songs using the playlist sorter
        if criteria == "title":
            sorted_songs = self.playlist_sorter.sort_by_title(songs, reverse, algorithm)
        elif criteria == "artist":
            sorted_songs = self.playlist_sorter.sort_by_artist(songs, reverse, algorithm)
        elif criteria == "duration":
            sorted_songs = self.playlist_sorter.sort_by_duration(songs, reverse, algorithm)
        elif criteria == "rating":
            sorted_songs = self.playlist_sorter.sort_by_rating(songs, reverse, algorithm)
        elif criteria == "date_added":
            sorted_songs = self.playlist_sorter.sort_by_date_added(songs, reverse, algorithm)
        elif criteria == "play_count":
            sorted_songs = self.playlist_sorter.sort_by_play_count(songs, reverse, algorithm)
        else:
            return False
        
        # Clear and rebuild the playlist with sorted songs
        self.playlist_engine.clear_playlist(playlist_id)
        for song in sorted_songs:
            self.playlist_engine.add_song(song, -1, playlist_id)
        
        return True
    
    def clean_duplicates(self, playlist_id: Optional[str] = None, 
                        strategy: str = "title_artist") -> Dict[str, Any]:
        """
        Clean duplicate songs from a playlist.
        
        Args:
            playlist_id: ID of playlist to clean (current if None)
            strategy: Duplicate detection strategy
            
        Returns:
            Dict: Cleaning results
        """
        songs = self.playlist_engine.get_songs(playlist_id)
        if not songs:
            return {"error": "No songs found"}
        
        # Set duplicate strategy
        self.auto_cleaner.set_duplicate_strategy(strategy)
        
        # Get duplicate statistics before cleaning
        stats_before = self.auto_cleaner.get_duplicate_stats(songs)
        
        # Clean duplicates
        cleaned_songs = self.auto_cleaner.clean_playlist_duplicates(songs)
        
        # Update playlist with cleaned songs
        self.playlist_engine.clear_playlist(playlist_id)
        for song in cleaned_songs:
            self.playlist_engine.add_song(song, -1, playlist_id)
        
        # Get statistics after cleaning
        stats_after = {
            "total_songs": len(cleaned_songs),
            "duplicates_removed": len(songs) - len(cleaned_songs)
        }
        
        return {
            "before": stats_before,
            "after": stats_after,
            "strategy_used": strategy
        }
    
    def get_recommendations(self, limit: int = 10) -> List[Song]:
        """
        Get song recommendations based on listening history and ratings.
        
        Args:
            limit: Number of recommendations to return
            
        Returns:
            List[Song]: Recommended songs
        """
        recommendations = []
        
        # Get top favorites
        top_favorites = self.favorites_queue.get_top_songs(limit // 2)
        favorite_songs = [fav['song'] for fav in top_favorites]
        
        # Get top rated songs not in favorites
        top_rated = self.song_rating_tree.get_top_rated_songs(limit)
        
        # Combine and deduplicate
        combined = favorite_songs + [song.to_dict() for song in top_rated]
        seen_ids = set()
        
        for song_data in combined:
            if isinstance(song_data, dict):
                song_id = song_data['id']
            else:
                song_id = song_data.id
                
            if song_id not in seen_ids and len(recommendations) < limit:
                if isinstance(song_data, dict):
                    song = self.song_lookup.get_song(song_id)
                    if song:
                        recommendations.append(song)
                else:
                    recommendations.append(song_data)
                seen_ids.add(song_id)
        
        return recommendations
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get comprehensive dashboard data."""
        return self.system_snapshot.generate_snapshot()
    
    def undo_last_play(self) -> Optional[Song]:
        """Undo the last played song."""
        return self.playback_history.undo_last_play()
    
    def get_playlist_info(self, playlist_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Get detailed information about a playlist."""
        playlist = self.playlist_engine.get_playlist(playlist_id) or self.playlist_engine.get_current_playlist()
        if playlist:
            return playlist.to_dict()
        return None
    
    def export_playlist(self, playlist_id: Optional[str] = None, format: str = "json") -> Optional[str]:
        """Export a playlist in the specified format."""
        playlist_data = self.get_playlist_info(playlist_id)
        if not playlist_data:
            return None
        
        if format == "json":
            import json
            return json.dumps(playlist_data, indent=2, default=str)
        elif format == "m3u":
            # Simple M3U format
            m3u_content = "#EXTM3U\n"
            for song in playlist_data['songs']:
                m3u_content += f"#EXTINF:{song['duration']},{song['artist']} - {song['title']}\n"
                m3u_content += f"# Song ID: {song['id']}\n"  # Placeholder for file path
            return m3u_content
        
        return None
    
    def get_engine_stats(self) -> Dict[str, Any]:
        """Get comprehensive engine statistics."""
        return {
            "version": self.version,
            "initialized": self.initialized,
            "total_songs": self.song_lookup.get_song_count(),
            "total_playlists": len(self.playlist_engine.playlists),
            "playback_history_size": self.playback_history.get_history_size(),
            "favorites_count": len(self.favorites_queue.heap),
            "rating_distribution": self.song_rating_tree.get_rating_distribution(),
            "component_status": {
                "playlist_engine": bool(self.playlist_engine),
                "playback_history": bool(self.playback_history),
                "song_rating_tree": bool(self.song_rating_tree),
                "song_lookup": bool(self.song_lookup),
                "playlist_sorter": bool(self.playlist_sorter),
                "auto_cleaner": bool(self.auto_cleaner),
                "favorites_queue": bool(self.favorites_queue),
                "system_snapshot": bool(self.system_snapshot)
            }
        }
