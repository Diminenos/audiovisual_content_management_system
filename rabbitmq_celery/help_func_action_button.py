import subprocess
import logging
import logger_config

# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)

# Function to extract FPS using ffprobe
def get_fps(video_path):
    try:
        # Run ffprobe command to get frame rate
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=r_frame_rate',
             '-of', 'default=noprint_wrappers=1:nokey=1', video_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        if result.returncode != 0:
            logger.error(f"Error getting FPS: {result.stderr}")
            return None

        fps_string = result.stdout.strip()
        numerator, denominator = map(int, fps_string.split('/'))
        fps = numerator / denominator
        logger.info(f"FPS extracted: {fps}")
        return fps
    except Exception as e:
        logger.error(f"An error occurred while getting FPS: {e}")
        return None


# Function to filter predictions and track first occurrence times
def filter_predictions(data):
    output_data = {}
    first_occurrences = {}

    for time, activities in data.items():
        try:
            if isinstance(activities, dict):
                # Get the first activity in the current time frame
                current_prediction = next(iter(activities.items()), None)

                if current_prediction:
                    activity_name, score = current_prediction
                    if activity_name not in first_occurrences:
                        # Store the first occurrence time and prediction
                        first_occurrences[activity_name] = time
                        output_data[time] = {activity_name: score}
                    # Optional: Update output data to keep only the first occurrence
                    elif first_occurrences[activity_name] == time:
                        output_data[time] = {activity_name: score}
            else:
                logger.warning(f"Expected a dictionary for time {time}, but got {type(activities).__name__}. Skipping this entry.")
        except Exception as e:
            logger.error(f"An error occurred while processing time {time}: {e}")

    return first_occurrences, output_data


def convert_json_format(data):
    output_data = {}
    
    for time, activities in data.items():
        try:
            if isinstance(activities, dict):
                # Create a dictionary for each second
                activity_dict = {}
                
                for index, activity in activities.items():
                    try:
                        # Split activity to extract name and score
                        activity_name, score = activity.split(": ")
                        score_value = float(score)  # Convert score to float
                        
                        
                        if score_value > 0.8:
                            # Add the activity to the dictionary with the score
                            activity_dict[activity_name] = f"{activity_name}: {score}"
                    except ValueError as ve:
                        logger.error(f"ValueError while processing activity {activity}: {ve}")
                    except Exception as e:
                        logger.error(f"An error occurred while processing activity {activity}: {e}")

                # Only add the time's activity dictionary if it has any entries
                if activity_dict:
                    output_data[time] = activity_dict
        except Exception as e:
            logger.error(f"An error occurred while processing time {time}: {e}")

    return output_data