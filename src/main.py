"""
Main entry point for PlayWise Music Playlist Management Engine
Can be run as standalone app or API server
"""

import sys
import os
from typing import Dict, Any

import uvicorn
from fastapi import FastAPI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from playwise_engine import PlayWiseEngine

def run_demo():
    """Run a demonstration of the PlayWise engine capabilities."""
    print("🎵 PlayWise Music Playlist Management Engine Demo")
    print("=" * 50)
    
    engine = PlayWiseEngine()
    print(f"✅ Engine initialized (version {engine.version})")
    
    print("\n📀 Creating sample songs...")
    songs_data = [
        ("Bohemian Rhapsody", "Queen", 355, 5),
        ("Hotel California", "Eagles", 391, 5),
        ("Stairway to Heaven", "Led Zeppelin", 482, 5),
        ("Imagine", "John Lennon", 183, 4),
        ("Billie Jean", "Michael Jackson", 294, 4),
        ("Sweet Child O' Mine", "Guns N' Roses", 356, 4),
        ("Smells Like Teen Spirit", "Nirvana", 302, 3),
        ("Wonderwall", "Oasis", 258, 3),
        ("Yesterday", "The Beatles", 125, 5),
        ("Purple Haze", "Jimi Hendrix", 170, 4)
    ]
    
    created_songs = []
    for title, artist, duration, rating in songs_data:
        song = engine.create_song(title, artist, duration, rating)
        created_songs.append(song)
        print(f"  ✅ {title} by {artist}")
    
    # Create playlists
    print("\n📝 Creating playlists...")
    classic_rock_id = engine.create_playlist("Classic Rock Hits", "The best of classic rock")
    favorites_id = engine.create_playlist("My Favorites", "Personal favorite songs")
    print(f"  ✅ Classic Rock Hits (ID: {classic_rock_id[:8]}...)")
    print(f"  ✅ My Favorites (ID: {favorites_id[:8]}...)")
    
    # Add songs to playlists
    print("\n➕ Adding songs to playlists...")
    for i, song in enumerate(created_songs[:6]):
        engine.add_song_to_playlist(song.id, classic_rock_id)
        if song.rating >= 4:
            engine.add_song_to_playlist(song.id, favorites_id)
    
    # Simulate some playback
    print("\n▶️  Simulating playback...")
    for song in created_songs[:5]:
        engine.play_song(song.id, song.duration - 30)  # Listened to most of the song
    
    # Sort a playlist
    print("\n🔄 Sorting playlist by rating (descending)...")
    engine.sort_playlist("rating", reverse=True, playlist_id=classic_rock_id)
    
    # Clean duplicates (simulate by adding duplicate)
    duplicate_song = engine.create_song("Bohemian Rhapsody", "Queen", 355, 5)
    engine.add_song_to_playlist(duplicate_song.id, classic_rock_id)
    print("\n🧹 Cleaning duplicates...")
    clean_result = engine.clean_duplicates(classic_rock_id)
    print(f"  ✅ Removed {clean_result.get('after', {}).get('duplicates_removed', 0)} duplicates")
    
    # Get recommendations
    print("\n💡 Getting recommendations...")
    recommendations = engine.get_recommendations(5)
    for song in recommendations:
        print(f"  🎵 {song.title} by {song.artist}")
    
    # Show dashboard data
    print("\n📊 Dashboard Summary:")
    dashboard = engine.get_dashboard_data()
    system_overview = dashboard.get('system_overview', {})
    print(f"  📀 Total Songs: {system_overview.get('total_songs', 0)}")
    print(f"  📝 Total Playlists: {system_overview.get('total_playlists', 0)}")
    print(f"  🎤 Unique Artists: {system_overview.get('total_unique_artists', 0)}")
    
    # Show playlist info
    print("\n📋 Playlist Details:")
    playlist_info = engine.get_playlist_info(classic_rock_id)
    if playlist_info:
        print(f"  📝 {playlist_info['name']}: {playlist_info['song_count']} songs, "
              f"{playlist_info['total_duration']//60:.1f} minutes")
    
    # Show recent history
    print("\n🕐 Recent Playback History:")
    history = engine.playback_history.get_recent_history(3)
    for song in history:
        print(f"  ▶️  {song.title} by {song.artist}")
    
    # Show favorites
    print("\n⭐ Top Favorites:")
    favorites = engine.favorites_queue.get_top_songs(3)
    for fav in favorites:
        song_info = fav['song']
        print(f"  ⭐ {song_info['title']} by {song_info['artist']} "
              f"(listened: {fav['listen_time']}s)")
    
    # Show rating distribution
    print("\n⭐ Rating Distribution:")
    distribution = engine.song_rating_tree.get_rating_distribution()
    for rating in sorted(distribution.keys(), reverse=True):
        stars = "⭐" * rating if rating > 0 else "☆"
        print(f"  {stars} ({rating}): {distribution[rating]} songs")
    
    print("\n🎉 Demo completed! All features working correctly.")
    return engine

def run_api_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = True):
    """Run the FastAPI server."""
    
    print("🚀 Starting PlayWise API server...")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"📖 API documentation: http://{host}:{port}/docs")
    print(f"📄 Alternative docs: http://{host}:{port}/redoc")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "api:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def show_help():
    """Show help information."""
    print("🎵 PlayWise Music Playlist Management Engine")
    print("=" * 50)
    print("Usage: python main.py [command] [options]")
    print("\nCommands:")
    print("  demo          Run a demonstration of engine capabilities")
    print("  api           Start the FastAPI server (default)")
    print("  help          Show this help message")
    print("\nAPI Server Options:")
    print("  --host HOST   Host to bind to (default: 0.0.0.0)")
    print("  --port PORT   Port to bind to (default: 8000)")
    print("  --no-reload   Disable auto-reload in development")
    print("\nExamples:")
    print("  python main.py demo")
    print("  python main.py api")
    print("  python main.py api --host localhost --port 8080")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="PlayWise Music Playlist Management Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "command", 
        nargs="?", 
        default="api",
        choices=["demo", "api", "help"],
        help="Command to run (default: api)"
    )
    
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind API server to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to bind API server to (default: 8000)"
    )
    
    parser.add_argument(
        "--no-reload",
        action="store_true",
        help="Disable auto-reload for API server"
    )
    
    args = parser.parse_args()
    
    if args.command == "help":
        show_help()
    elif args.command == "demo":
        run_demo()
    elif args.command == "api":
        run_api_server(
            host=args.host,
            port=args.port,
            reload=not args.no_reload
        )
    else:
        print(f"Unknown command: {args.command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
