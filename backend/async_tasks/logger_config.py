import logging

from logging.handlers import TimedRotatingFileHandler
# Keep one week of logs
handler = TimedRotatingFileHandler(
    '/home/dimineno/consumer_celery/app.log', 
    when='midnight', 
    interval=1, 
    backupCount=7 
)
def setup_logging():
    logging.basicConfig(
        handlers=[handler],
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
