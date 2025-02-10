import logging
import logger_config
import sys
from predict_static_video import is_static_video
from video_updates import update_content_type
# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)



if __name__ == '__main__':
    
    post_id = sys.argv[1]  
    file_path = sys.argv[2]
 # Check if the file extension is .mp4
    if not file_path.lower().endswith('.mp4'):
        logger.info(f"Audio file format. Updating content_type to 'audio'.")
        update_content_type(post_id, is_audio=True)
    else:
        # Check if video is static before running action recognition
        if is_static_video(file_path):
            logger.info("Video is static. Updating content_type to 'audio'.")
            update_content_type(post_id, is_audio=True)
        else:
            logger.info("Video is dynamic. Updating content_type to 'video'.")
            update_content_type(post_id, is_audio=False)