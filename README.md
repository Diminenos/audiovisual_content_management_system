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
  Extracts topics/entities from subtitles for semantic search.

- **Asynchronous Processing**  
  Tasks are processed in the background using Celery and RabbitMQ.

- **WordPress Integration**  
  WordPress plugin + theme for enhanced video playback with tags, topics, and subtitles.

---

## Tech Stack

### Backend
- Python 3.10+, Celery, RabbitMQ
- ffmpeg, pydub
- Whisper (OpenAI)
- MMAction2 (from OpenMMLab)
- spaCy or Hugging Face (NER)

### Frontend
- WordPress (Custom Plugin + Child Theme)
- PHP, HTML, JS, CSS

---


## Deployment Notes

This system was deployed on a Linux server running:

- Python 3.10
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
- Hugging Face
- spaCy
