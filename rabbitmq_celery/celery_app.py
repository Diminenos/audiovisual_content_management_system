from celery import Celery
import subprocess
import logging
import gc
import logger_config
import os
from dotenv import load_dotenv


# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)


# Load environment variables
load_dotenv()

# Build the RabbitMQ URL securely
RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST")
RABBITMQ_PORT = os.getenv("RABBITMQ_PORT")
RABBITMQ_VIRTUAL_HOST = os.getenv("RABBITMQ_VIRTUAL_HOST")

BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:{RABBITMQ_PORT}/{RABBITMQ_VIRTUAL_HOST}"

# Initialize Celery app
app = Celery('video_processing', broker=BROKER_URL)
# Other configurations


# Configure Celery settings
app.conf.update(
    worker_concurrency=1,  # This ensures only 1 worker processes a task at a time
    worker_prefetch_multiplier=1,  # Ensures only 1 task is fetched at a time
    broker_connection_retry_on_startup=True,
)

app.conf.task_reject_on_worker_lost = True
app.conf.worker_prefetch_multiplier = 1
app.conf.broker_transport_options = {'visibility_timeout': 3600}  # 1 hour
app.conf.acks_late=True

# Function to run the algorithms sequentially
def run_algorithm(post_id, file_path, script_name):
    try:
        # Choose the Python interpreter based on the script being run
        if script_name == "ner_algo.py":
            python_executable = "/home/dimineno/miniconda3/envs/entityRec/bin/python"
        else:
            python_executable = "/home/dimineno/miniconda3/envs/arutvEnv/bin/python"
        
        # Run the algorithm using the appropriate Python interpreter
        result = subprocess.run(
            [python_executable, script_name, str(post_id), file_path],
            capture_output=True, text=True
        )
        
        if result.returncode == 0:
            logger.info(f"{script_name} completed for post ID: {post_id}")
        else:
            logger.error(f"{script_name} failed for post ID: {post_id}. Error: {result.stderr}")

    except subprocess.TimeoutExpired:
        logger.error(f"{script_name} timed out for post ID: {post_id}")
    except Exception as e:
        logger.exception(f"Error running {script_name} for post ID {post_id}: {e}")
    finally:
        gc.collect()

# Celery task to process video sequentially
@app.task(bind=True, acks_late=True, task_reject_on_worker_lost=True, max_retries=3, retry_backoff=True)
def process_video(self, post_id, file_path):
    try:
        algorithms = [
            "seperate_audio_video.py",
            "audio_tag_algo.py", 
            "create_subs_algo.py", 
            "ner_algo.py",  # This will run in the entity_ner conda env
            "action_recognition_algo.py"
        ]
        
        for script in algorithms:
            run_algorithm(post_id, file_path, script)

        return f"Video {post_id} processed successfully!"
    except Exception as e:
        self.retry(exc=e)