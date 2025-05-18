# systemd Services 

This folder contains `systemd` service unit files used to run background processing components of the Aristotle TV system on startup.

These services ensure that:
- The **RabbitMQ consumer** stays online and listens for new tasks.
- The **Celery worker** automatically processes video/audio processing pipelines in the background.


##  Notes

- Restart behavior is configured for resilience (`Restart=always` and `RestartSec=5s`).
- These services allow the backend to operate continuously without manual reboots or script starts.

