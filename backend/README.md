# Backend – Aristotle TV

This directory contains all the backend logic for the Aristotle TV audiovisual content management system.

It includes machine learning pipelines for processing audio and video, NLP models for speech analysis, and asynchronous background task infrastructure.

The system was built from scratch in a virtual machine hosted by Aristotle University.

## Modules

### audio_classification/
- Train and test custom audio classifier
- Outputs a `.pkl` model used for prediction


### async_tasks/
- Celery workers process tasks in the background
- RabbitMQ to queue tasks

### deployment/
– Systemd service files to run components on boot

### 🔗 wordpress_integration/
- Creates a custom plugin that works as a message producer.
- Producer sends a json file with an id and file path to the consumer



