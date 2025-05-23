# Aristotle TV – Audiovisual Content Management System 

This is my thesis project at Aristotle University.  
The system processes and enhances audiovisual content using machine learning and natural language processing.



---

## Features

- **Audio Classification**  
  Custom-trained model to detect music, speech, etc.

- **Action Recognition (MMAction2)**  
  Detects actions in videos using pretrained models.  
  Adds clickable timestamps for navigation.

- **Speech-to-Text with Whisper**  
  Transcribes spoken audio into text and subtitles.

- **Named Entity Recognition (NER)**  
  Extracts topics/entities from text for semantic search.

- **Asynchronous Processing**  
  Tasks (Algorithms) are processed in the background using Celery and RabbitMQ.

- **WordPress Integration**  
  WordPress plugin + theme for enhanced video playback with tags, topics, and subtitles.

---

## Tech Stack

### Backend
- Python, Celery, RabbitMQ
- ffmpeg, pydub
- Whisper (OpenAI)
- MMAction2 (from OpenMMLab)
- spaCy (NER)

### Frontend
- WordPress (Custom Plugin + Child Theme)
- PHP, HTML, JS, CSS

---


## Deployment Notes

This system was deployed on a Linux server running:

- Python
- Celery workers
- RabbitMQ (as system service)
- PHP + WordPress
- Custom systemd services

See [`deployment/systemd/`](deployment/systemd/) for service file setup.

---


## Thesis Background

This system supports educational media archives by:

- Classifying audio & actions in video
- Creating timestamp-based video navigation
- Extracting semantic topics for search
- Enhancing WordPress-based content with ML/NLP

---

## License & Credits

This project is for academic use.  
Inspired by tools from:
- OpenAI (Whisper)
- OpenMMLab (MMAction2)
- spaCy

## Alternate Architecture (Django First Attempt)

Before switching to WordPress, this system was initially prototyped in Django.

- Located in: `/django_first_try/`
- Demonstrates user authentication, media upload, and early backend logic
- Dropped in favor of WordPress to ensure usability of the system for both technical and non-technical users
