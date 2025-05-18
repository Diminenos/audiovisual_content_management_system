import pika
import json
from celery_app import process_video
import logging
import logger_config
import functools

logger_config.setup_logging()
logger = logging.getLogger(__name__)

# Function to acknowledge message
def ack_message(ch, delivery_tag):
    if ch.is_open:
        ch.basic_ack(delivery_tag)
    else:
        pass

# Function to handle incoming messages from RabbitMQ and call Celery task
def on_message_received(ch, method, properties, body):
    post_id = None
    file_path = None
    
    try:
        # Parse the message
        message = json.loads(body.decode('utf-8'))
        post_id = message['post_id']
        file_path = message['file_path']
        logger.info(f'Received new message: {file_path}, post ID: {post_id}')
        
        # Call Celery task to process the video
        process_video.apply_async((post_id, file_path))
        logger.info(f"Task submitted to Celery for post ID: {post_id}")

    except json.JSONDecodeError as e:
        logger.exception(f"JSON decoding error: {e} for message: {body}")
    except Exception as e:
        logger.exception(f"Error processing message: {e}")
    
    finally:
        # Acknowledge the message
        if post_id is not None:
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"Acknowledged message for post ID: {post_id}")


# Main function to start consuming messages from RabbitMQ
def main():
    # Set up RabbitMQ connection parameters
    credentials = pika.PlainCredentials('dimineno', 'aristotle1997')
    parameters = pika.ConnectionParameters('localhost', 5672, 'videos', credentials, heartbeat=600, blocked_connection_timeout=300)

    try:
        # Establish connection to RabbitMQ
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        # Declare  queue
        channel.exchange_declare(exchange='algo_exchange', exchange_type='fanout', durable=True)
        result = channel.queue_declare(queue='algo_queue',durable=True)

        queue_name = result.method.queue
        channel.queue_bind(exchange='algo_exchange', queue=queue_name)
        channel.basic_qos(prefetch_count=1)  

        logger.info(' [*] Waiting for messages. To exit press CTRL+C')

        
        channel.basic_consume(queue=queue_name, on_message_callback=on_message_received)

      
        channel.start_consuming()

    except pika.exceptions.AMQPConnectionError:
        logger.error("Connection to RabbitMQ failed. Retrying...")
        main()  

if __name__ == '__main__':
    main()
