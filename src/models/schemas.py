"""
Pydantic schemas for API request/response models
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class SortAlgorithm(str, Enum):
    """Supported sorting algorithms"""
    MERGE = "merge"
    QUICK = "quick"
    BUILTIN = "builtin"

class SortCriteria(str, Enum):
    """Supported sorting criteria"""
    TITLE = "title"
    ARTIST = "artist"
    DURATION = "duration"
    RATING = "rating"
    DATE_ADDED = "date_added"
    PLAY_COUNT = "play_count"

class SongCreate(BaseModel):
    """Schema for creating a new song"""
    title: str = Field(..., min_length=1, max_length=200)
    artist: str = Field(..., min_length=1, max_length=200)
    duration: int = Field(..., gt=0, description="Duration in seconds")
    rating: int = Field(default=0, ge=0, le=5)

class SongUpdate(BaseModel):
    """Schema for updating an existing song"""
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    artist: Optional[str] = Field(None, min_length=1, max_length=200)
    duration: Optional[int] = Field(None, gt=0)
    rating: Optional[int] = Field(None, ge=0, le=5)

class SongResponse(BaseModel):
    """Schema for song API responses"""
    id: str
    title: str
    artist: str
    duration: int
    rating: int
    date_added: str
    listen_time: int
    play_count: int

class PlaylistCreate(BaseModel):
    """Schema for creating a playlist"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(default="", max_length=500)

class PlaylistResponse(BaseModel):
    """Schema for playlist responses"""
    id: str
    name: str
    description: str
    songs: List[SongResponse]
    total_duration: int
    song_count: int
    created_at: str

class SortRequest(BaseModel):
    """Schema for sorting requests"""
    criteria: SortCriteria
    reverse: bool = False
    algorithm: SortAlgorithm = SortAlgorithm.BUILTIN

class MoveRequest(BaseModel):
    """Schema for moving songs in playlist"""
    from_index: int = Field(..., ge=0)
    to_index: int = Field(..., ge=0)

class RatingSearchRequest(BaseModel):
    """Schema for rating-based search"""
    min_rating: int = Field(default=1, ge=0, le=5)
    max_rating: int = Field(default=5, ge=0, le=5)

class SystemStatsResponse(BaseModel):
    """Schema for system statistics"""
    total_songs: int
    total_playlists: int
    top_longest_songs: List[SongResponse]
    recently_played: List[SongResponse]
    rating_distribution: Dict[str, int]
    playlist_statistics: Dict[str, Any]
    top_favorites: List[Dict[str, Any]]

class ErrorResponse(BaseModel):
    """Schema for error responses"""
    error: str
    detail: Optional[str] = None
    
class SuccessResponse(BaseModel):
    """Schema for success responses"""
    message: str
    data: Optional[Any] = None
