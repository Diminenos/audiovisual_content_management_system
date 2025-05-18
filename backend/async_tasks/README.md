# Celery & RabbitMQ Backend Processor

This folder contains the asynchronous backend logic for Aristotle TV, built using **Celery** and **RabbitMQ**. It coordinates the execution of all video/audio processing algorithms in the pipeline and communicates the results to a WordPress frontend.

---

## Overview

- Listens for messages published via RabbitMQ (e.g., new media upload events).
- Passes file data to a Celery worker.
- Runs a series of ML-based scripts to classify, transcribe, and tag media.
- Updates results to WordPress via its REST API using environment-based credentials.

---

## Key Files

- `celery_app.py`:  
  Defines the Celery application and task `process_video`.  
  Runs each script in sequence using `subprocess`.

- `consumer.py`:  
  RabbitMQ consumer that listens for messages and submits tasks to Celery.

- `.env`:  
  Stores sensitive information like WordPress API credentials (not included in repo).

---

## Workflow

1. WordPress or an external producer publishes a message to RabbitMQ with:
   ```json
   {
     "post_id": 123,
     "file_path": "/path/to/media/file.mp4"
   }
   ```

2. `consumer.py` receives the message and calls `process_video` via Celery.

3. Celery runs the following scripts **in order**:
   - `seperate_audio_video.py`
   - `audio_tag_algo.py`
   - `create_subs_algo.py`
   - `ner_algo.py`
   - `action_recognition_algo.py`

4. Each script is executed in a separate Conda environment, where necessary.

5. Results are pushed to the WordPress database using its REST API (video_updates.py).


## Notes

- Only one task is processed at a time (concurrency=1) to limit resource usage and ensure sequential, stable execution on a low-resource server.
- All subprocess calls are logged and garbage-collected after execution
- Robust retry logic is implemented in Celery for failed tasks

