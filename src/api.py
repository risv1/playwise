"""
FastAPI application for PlayWise Music Playlist Management Engine
Provides REST API endpoints for all engine functionality
"""

from fastapi import FastAPI, HTTPException, Query, Path, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
import uvicorn
from datetime import datetime

from playwise_engine import PlayWiseEngine
from models.schemas import (
    SongCreate, SongUpdate, SongResponse, PlaylistCreate, PlaylistResponse,
    SortRequest, MoveRequest, RatingSearchRequest, SystemStatsResponse,
    ErrorResponse, SuccessResponse, SortAlgorithm, SortCriteria
)
from models.song import Song

# Initialize FastAPI app
app = FastAPI(
    title="PlayWise Music Playlist Management API",
    description="Smart music playlist management engine with advanced data structures and algorithms",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the PlayWise engine
playwise_engine = PlayWiseEngine()

# Custom exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# Root endpoint
@app.get("/", response_model=Dict[str, Any])
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to PlayWise Music Playlist Management API",
        "version": "1.0.0",
        "docs": "/docs",
        "engine_stats": playwise_engine.get_engine_stats(),
        "timestamp": datetime.now().isoformat()
    }

# Health check endpoint
@app.get("/health", response_model=Dict[str, str])
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engine_initialized": str(playwise_engine.initialized)
    }

# ========== SONG MANAGEMENT ENDPOINTS ==========

@app.post("/songs", response_model=SongResponse, status_code=201)
async def create_song(song_data: SongCreate):
    """Create a new song."""
    try:
        song = playwise_engine.create_song(
            title=song_data.title,
            artist=song_data.artist,
            duration=song_data.duration,
            rating=song_data.rating
        )
        return song.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create song: {str(e)}")

@app.get("/songs", response_model=List[SongResponse])
async def get_all_songs(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all songs with pagination."""
    try:
        all_songs = playwise_engine.song_lookup.get_all_songs()
        total_songs = len(all_songs)
        
        # Apply pagination
        paginated_songs = all_songs[offset:offset + limit]
        
        return [song.to_dict() for song in paginated_songs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve songs: {str(e)}")

@app.get("/songs/{song_id}", response_model=SongResponse)
async def get_song(song_id: str = Path(..., description="Song ID")):
    """Get a specific song by ID."""
    song = playwise_engine.song_lookup.get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song.to_dict()

@app.put("/songs/{song_id}", response_model=SongResponse)
async def update_song(
    song_id: str = Path(..., description="Song ID"),
    song_update: SongUpdate = Body(...)
):
    """Update a song."""
    song = playwise_engine.song_lookup.get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Update song fields
    if song_update.title is not None:
        song.title = song_update.title
    if song_update.artist is not None:
        song.artist = song_update.artist
    if song_update.duration is not None:
        song.duration = song_update.duration
    if song_update.rating is not None:
        song.update_rating(song_update.rating)
    
    # Update in lookup system
    playwise_engine.song_lookup.update_song(song)
    
    return song.to_dict()

@app.delete("/songs/{song_id}", response_model=SuccessResponse)
async def delete_song(song_id: str = Path(..., description="Song ID")):
    """Delete a song."""
    song = playwise_engine.song_lookup.get_song(song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    
    # Remove from all systems
    playwise_engine.song_lookup.remove_song(song)
    playwise_engine.song_rating_tree.delete_song(song_id)
    playwise_engine.favorites_queue.remove_song(song_id)
    
    return SuccessResponse(message="Song deleted successfully")

# ========== SONG SEARCH ENDPOINTS ==========

@app.get("/songs/search/title", response_model=List[SongResponse])
async def search_songs_by_title(
    query: str = Query(..., min_length=1, description="Title search query"),
    exact: bool = Query(False, description="Exact match vs fuzzy search")
):
    """Search songs by title."""
    try:
        if exact:
            songs = playwise_engine.song_lookup.search_by_title(query)
        else:
            songs = playwise_engine.song_lookup.fuzzy_search_title(query)
        
        return [song.to_dict() for song in songs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/songs/search/artist", response_model=List[SongResponse])
async def search_songs_by_artist(
    query: str = Query(..., min_length=1, description="Artist search query"),
    exact: bool = Query(False, description="Exact match vs fuzzy search")
):
    """Search songs by artist."""
    try:
        if exact:
            songs = playwise_engine.song_lookup.search_by_artist(query)
        else:
            songs = playwise_engine.song_lookup.fuzzy_search_artist(query)
        
        return [song.to_dict() for song in songs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/songs/search", response_model=List[SongResponse])
async def search_songs(
    query: str = Query(..., min_length=1, description="General search query"),
    search_type: str = Query("all", regex="^(title|artist|all)$")
):
    """General song search."""
    try:
        songs = playwise_engine.search_songs(query, search_type)
        return [song.to_dict() for song in songs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.post("/songs/search/rating", response_model=List[SongResponse])
async def search_songs_by_rating(search_params: RatingSearchRequest):
    """Search songs by rating range."""
    try:
        songs = playwise_engine.get_songs_by_rating(
            search_params.min_rating,
            search_params.max_rating
        )
        return [song.to_dict() for song in songs]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rating search failed: {str(e)}")

# ========== PLAYLIST MANAGEMENT ENDPOINTS ==========

@app.post("/playlists", response_model=Dict[str, str], status_code=201)
async def create_playlist(playlist_data: PlaylistCreate):
    """Create a new playlist."""
    try:
        playlist_id = playwise_engine.create_playlist(
            name=playlist_data.name,
            description=playlist_data.description
        )
        return {"playlist_id": playlist_id, "message": "Playlist created successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create playlist: {str(e)}")

@app.get("/playlists", response_model=List[Dict[str, Any]])
async def get_all_playlists():
    """Get all playlists."""
    try:
        playlists = playwise_engine.playlist_engine.list_playlists()
        return [playlist.to_dict() for playlist in playlists]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve playlists: {str(e)}")

@app.get("/playlists/{playlist_id}", response_model=Dict[str, Any])
async def get_playlist(playlist_id: str = Path(..., description="Playlist ID")):
    """Get a specific playlist."""
    playlist_info = playwise_engine.get_playlist_info(playlist_id)
    if not playlist_info:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return playlist_info

@app.get("/playlists/current/info", response_model=Dict[str, Any])
async def get_current_playlist():
    """Get the current active playlist."""
    playlist_info = playwise_engine.get_playlist_info()
    if not playlist_info:
        raise HTTPException(status_code=404, detail="No current playlist set")
    return playlist_info

@app.put("/playlists/{playlist_id}/current", response_model=SuccessResponse)
async def set_current_playlist(playlist_id: str = Path(..., description="Playlist ID")):
    """Set the current active playlist."""
    success = playwise_engine.playlist_engine.set_current_playlist(playlist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return SuccessResponse(message="Current playlist updated successfully")

@app.delete("/playlists/{playlist_id}", response_model=SuccessResponse)
async def delete_playlist(playlist_id: str = Path(..., description="Playlist ID")):
    """Delete a playlist."""
    success = playwise_engine.playlist_engine.delete_playlist(playlist_id)
    if not success:
        raise HTTPException(status_code=404, detail="Playlist not found")
    return SuccessResponse(message="Playlist deleted successfully")

# ========== PLAYLIST SONG MANAGEMENT ENDPOINTS ==========

@app.post("/playlists/{playlist_id}/songs/{song_id}", response_model=SuccessResponse)
async def add_song_to_playlist(
    playlist_id: str = Path(..., description="Playlist ID"),
    song_id: str = Path(..., description="Song ID"),
    position: int = Query(-1, description="Position to insert song (-1 for end)")
):
    """Add a song to a playlist."""
    success = playwise_engine.add_song_to_playlist(song_id, playlist_id, position)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to add song to playlist")
    return SuccessResponse(message="Song added to playlist successfully")

@app.delete("/playlists/{playlist_id}/songs/{song_index}", response_model=SuccessResponse)
async def remove_song_from_playlist(
    playlist_id: str = Path(..., description="Playlist ID"),
    song_index: int = Path(..., ge=0, description="Song index in playlist")
):
    """Remove a song from a playlist."""
    removed_song = playwise_engine.playlist_engine.delete_song(song_index, playlist_id)
    if not removed_song:
        raise HTTPException(status_code=400, detail="Failed to remove song from playlist")
    return SuccessResponse(message="Song removed from playlist successfully")

@app.put("/playlists/{playlist_id}/songs/move", response_model=SuccessResponse)
async def move_song_in_playlist(
    playlist_id: str = Path(..., description="Playlist ID"),
    move_request: MoveRequest = Body(...)
):
    """Move a song within a playlist."""
    success = playwise_engine.playlist_engine.move_song(
        move_request.from_index,
        move_request.to_index,
        playlist_id
    )
    if not success:
        raise HTTPException(status_code=400, detail="Failed to move song in playlist")
    return SuccessResponse(message="Song moved successfully")

@app.put("/playlists/{playlist_id}/reverse", response_model=SuccessResponse)
async def reverse_playlist(playlist_id: str = Path(..., description="Playlist ID")):
    """Reverse the order of songs in a playlist."""
    success = playwise_engine.playlist_engine.reverse_playlist(playlist_id)
    if not success:
        raise HTTPException(status_code=400, detail="Failed to reverse playlist")
    return SuccessResponse(message="Playlist reversed successfully")

# ========== PLAYLIST SORTING ENDPOINTS ==========

@app.post("/playlists/{playlist_id}/sort", response_model=Dict[str, Any])
async def sort_playlist(
    playlist_id: str = Path(..., description="Playlist ID"),
    sort_request: SortRequest = Body(...)
):
    """Sort a playlist by specified criteria."""
    try:
        success = playwise_engine.sort_playlist(
            criteria=sort_request.criteria.value,
            reverse=sort_request.reverse,
            algorithm=sort_request.algorithm.value,
            playlist_id=playlist_id
        )
        
        if not success:
            raise HTTPException(status_code=400, detail="Failed to sort playlist")
        
        # Get performance stats
        sort_time = playwise_engine.playlist_sorter.get_last_sort_time()
        
        return {
            "message": "Playlist sorted successfully",
            "criteria": sort_request.criteria.value,
            "algorithm": sort_request.algorithm.value,
            "reverse": sort_request.reverse,
            "sort_time_seconds": sort_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sorting failed: {str(e)}")

@app.get("/sorting/performance", response_model=Dict[str, Any])
async def get_sorting_performance():
    """Get sorting algorithm performance statistics."""
    return playwise_engine.playlist_sorter.get_performance_stats()

# ========== PLAYBACK ENDPOINTS ==========

@app.post("/playback/play/{song_id}", response_model=SuccessResponse)
async def play_song(
    song_id: str = Path(..., description="Song ID"),
    listen_duration: Optional[int] = Query(None, ge=0, description="Listen duration in seconds")
):
    """Play a song and update playback history."""
    success = playwise_engine.play_song(song_id, listen_duration)
    if not success:
        raise HTTPException(status_code=404, detail="Song not found")
    return SuccessResponse(message="Song played and recorded in history")

@app.get("/playback/history", response_model=List[SongResponse])
async def get_playback_history(limit: int = Query(50, ge=1, le=100)):
    """Get recent playback history."""
    history = playwise_engine.playback_history.get_recent_history(limit)
    return [song.to_dict() for song in history]

@app.post("/playback/undo", response_model=Dict[str, Any])
async def undo_last_play():
    """Undo the last played song."""
    undone_song = playwise_engine.undo_last_play()
    if not undone_song:
        return {"message": "No song to undo", "undone_song": None}
    return {"message": "Last play undone", "undone_song": undone_song.to_dict()}

@app.get("/playback/most-played", response_model=List[SongResponse])
async def get_most_played_songs(limit: int = Query(10, ge=1, le=50)):
    """Get most played songs."""
    most_played = playwise_engine.playback_history.get_most_played_songs(limit)
    return [song.to_dict() for song in most_played]

# ========== RATING ENDPOINTS ==========

@app.put("/songs/{song_id}/rating", response_model=SuccessResponse)
async def rate_song(
    song_id: str = Path(..., description="Song ID"),
    rating: int = Query(..., ge=0, le=5, description="Song rating (0-5)")
):
    """Rate a song."""
    success = playwise_engine.rate_song(song_id, rating)
    if not success:
        raise HTTPException(status_code=404, detail="Song not found")
    return SuccessResponse(message=f"Song rated {rating} stars")

@app.get("/ratings/distribution", response_model=Dict[str, int])
async def get_rating_distribution():
    """Get rating distribution across all songs."""
    return playwise_engine.song_rating_tree.get_rating_distribution()

@app.get("/ratings/top-rated", response_model=List[SongResponse])
async def get_top_rated_songs(limit: int = Query(10, ge=1, le=50)):
    """Get top rated songs."""
    top_rated = playwise_engine.song_rating_tree.get_top_rated_songs(limit)
    return [song.to_dict() for song in top_rated]

# ========== FAVORITES ENDPOINTS ==========

@app.get("/favorites", response_model=List[Dict[str, Any]])
async def get_favorites(limit: int = Query(20, ge=1, le=100)):
    """Get favorite songs."""
    return playwise_engine.favorites_queue.get_top_songs(limit)

@app.get("/favorites/stats", response_model=Dict[str, Any])
async def get_favorites_stats():
    """Get favorites queue statistics."""
    return playwise_engine.favorites_queue.get_queue_stats()

@app.get("/favorites/recent", response_model=List[Dict[str, Any]])
async def get_recently_favorited(limit: int = Query(10, ge=1, le=50)):
    """Get recently favorited songs."""
    return playwise_engine.favorites_queue.get_recently_favorited(limit)

# ========== DUPLICATE CLEANING ENDPOINTS ==========

@app.post("/playlists/{playlist_id}/clean-duplicates", response_model=Dict[str, Any])
async def clean_playlist_duplicates(
    playlist_id: str = Path(..., description="Playlist ID"),
    strategy: str = Query("title_artist", regex="^(title_artist|title_artist_duration|title_only|strict)$")
):
    """Clean duplicate songs from a playlist."""
    try:
        result = playwise_engine.clean_duplicates(playlist_id, strategy)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Duplicate cleaning failed: {str(e)}")

@app.get("/duplicates/analyze/{playlist_id}", response_model=Dict[str, Any])
async def analyze_duplicates(
    playlist_id: str = Path(..., description="Playlist ID"),
    strategy: str = Query("title_artist", regex="^(title_artist|title_artist_duration|title_only|strict)$")
):
    """Analyze duplicates in a playlist without removing them."""
    songs = playwise_engine.playlist_engine.get_songs(playlist_id)
    if not songs:
        raise HTTPException(status_code=404, detail="Playlist not found or empty")
    
    playwise_engine.auto_cleaner.set_duplicate_strategy(strategy)
    stats = playwise_engine.auto_cleaner.get_duplicate_stats(songs)
    
    return stats

# ========== RECOMMENDATIONS ENDPOINTS ==========

@app.get("/recommendations", response_model=List[SongResponse])
async def get_recommendations(limit: int = Query(10, ge=1, le=50)):
    """Get song recommendations."""
    try:
        recommendations = playwise_engine.get_recommendations(limit)
        return [song.to_dict() for song in recommendations]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate recommendations: {str(e)}")

# ========== ANALYTICS AND DASHBOARD ENDPOINTS ==========

@app.get("/dashboard", response_model=Dict[str, Any])
async def get_dashboard_data():
    """Get comprehensive dashboard data."""
    try:
        return playwise_engine.get_dashboard_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate dashboard data: {str(e)}")

@app.get("/stats/system", response_model=Dict[str, Any])
async def get_system_stats():
    """Get comprehensive system statistics."""
    return playwise_engine.get_engine_stats()

@app.get("/export/playlist/{playlist_id}", response_model=Dict[str, str])
async def export_playlist(
    playlist_id: str = Path(..., description="Playlist ID"),
    format: str = Query("json", regex="^(json|m3u)$")
):
    """Export a playlist in the specified format."""
    try:
        exported_data = playwise_engine.export_playlist(playlist_id, format)
        if not exported_data:
            raise HTTPException(status_code=404, detail="Playlist not found")
        
        return {
            "format": format,
            "data": exported_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export failed: {str(e)}")

# ========== UTILITY ENDPOINTS ==========

@app.post("/admin/reset-stats", response_model=SuccessResponse)
async def reset_performance_stats():
    """Reset all performance statistics."""
    playwise_engine.playlist_sorter.reset_stats()
    playwise_engine.auto_cleaner.reset_stats()
    return SuccessResponse(message="Performance statistics reset successfully")

@app.get("/admin/cache/clear", response_model=SuccessResponse)
async def clear_caches():
    """Clear all system caches."""
    playwise_engine.system_snapshot.clear_cache()
    playwise_engine.auto_cleaner.clear_cache()
    return SuccessResponse(message="Caches cleared successfully")

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
