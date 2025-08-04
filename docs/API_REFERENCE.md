# API Reference for PlayWise Music Playlist Management Engine

## Overview

This document provides an API reference for the PlayWise music playlist management engine. It outlines the available classes, methods, and their usage within the system.

## Classes

### 1. PlaylistEngine

**Module**: `src/core/playlist_engine.py`

**Description**: Manages ordered song collections with methods for adding, deleting, and reordering songs.

**Methods**:
- `add_song(song, position=-1)`: Adds a song to the playlist at the specified position.
- `delete_song(index)`: Deletes a song from the playlist at the specified index.
- `move_song(from_idx, to_idx)`: Moves a song from one index to another.
- `reverse_playlist()`: Reverses the order of songs in the playlist.

### 2. PlaybackHistory

**Module**: `src/core/playback_history.py`

**Description**: Tracks recently played songs and provides undo functionality.

**Methods**:
- `add_to_history(song)`: Adds a song to the playback history.
- `undo_last_play()`: Undoes the last played song.
- `get_recent_history(k)`: Retrieves the last k played songs.

### 3. SongRatingTree

**Module**: `src/core/song_rating_tree.py`

**Description**: Organizes songs by rating and supports fast rating-based queries.

**Methods**:
- `insert_song(song, rating)`: Inserts a song with its rating into the tree.
- `search_by_rating(rating)`: Searches for songs by a specific rating.
- `delete_song(song_id)`: Deletes a song from the tree by its ID.
- `get_songs_by_rating_range()`: Retrieves songs within a specified rating range.

### 4. SongLookup

**Module**: `src/core/song_lookup.py`

**Description**: Provides instant retrieval of songs by ID, title, or artist.

**Methods**:
- `add_song(song)`: Adds a song to the lookup table.
- `get_song(song_id)`: Retrieves a song by its ID.
- `search_by_title(title)`: Searches for songs by title.
- `search_by_artist(artist)`: Searches for songs by artist.

### 5. PlaylistSorter

**Module**: `src/core/playlist_sorter.py`

**Description**: Implements various sorting algorithms for playlists.

**Methods**:
- `sort_by_title(songs, reverse, algorithm)`: Sorts songs by title using the specified algorithm.
- `sort_by_duration(songs, reverse, algorithm)`: Sorts songs by duration using the specified algorithm.
- `sort_by_date_added(songs, reverse, algorithm)`: Sorts songs by the date added using the specified algorithm.

### 6. AutoCleaner

**Module**: `src/core/auto_cleaner.py`

**Description**: Removes duplicate songs based on composite keys.

**Methods**:
- `remove_duplicates(songs)`: Removes duplicate songs from the provided list.
- `find_duplicates(songs)`: Finds duplicate songs in the provided list.

### 7. FavoritesQueue

**Module**: `src/core/favorites_queue.py`

**Description**: Maintains a sorted queue of favorite songs by listen time.

**Methods**:
- `add_song(song)`: Adds a song to the favorites queue.
- `update_listen_time(song_id, time)`: Updates the listen time for a specific song.
- `get_top_songs(count)`: Retrieves the top favorite songs based on listen time.

### 8. SystemSnapshot

**Module**: `src/core/system_snapshot.py`

**Description**: Generates real-time system statistics and insights.

**Methods**:
- `generate_snapshot()`: Generates a snapshot of the current system state, including statistics and insights.

## Usage

To use the PlayWise engine, import the necessary classes from their respective modules and instantiate them as needed. Refer to the individual class documentation for specific method usage and examples.
