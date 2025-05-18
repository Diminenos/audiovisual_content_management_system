# Frontend – Aristotle TV (WordPress)

This folder contains **only the frontend components that i develop** for Aristotle TV.
It consists of **custom plugins** and a **child theme** used to display enriched media posts with ML-generated results.

---


## Custom Plugin Functionality

The plugin directory includes three custom WordPress plugins developed for enhanced media interaction:

### 1. `user-files-display`
- Shows uploaded video/audio files for the currently logged-in user.

### 2. `thumbnail-generator`
- Automatically generates and displays thumbnails for each media file.

### 3. `topic-search-form`
- Adds a search interface for exploring content based on **topics** extracted by NER.
- Users can select a topic and search for specific keywords inside video/audio speech.

---

## Child Theme Overview

The `aristotle-child-theme/` extends an existing WordPress theme and adds:

- A **custom single post template** (`single-video.php`, etc.) to display:
  - Media player (audio or video)
  - Subtitles (from Whisper)
  - Action tag and navigation buttons (from MMAction2)
  - Audio tags




