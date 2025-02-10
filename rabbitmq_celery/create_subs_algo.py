import sys
sys.path.insert(0, '/opt/whisper-main/')
import whisper
import logging
import logger_config
from video_updates import update_greek_subs,update_english_subs,update_post_content
import json

# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)

def whisper_load_model():
    #Load the model of the whisper algorithm
    model = whisper.load_model("medium",device='cuda')
    return model

def whisper_algorithm(post_id,file_path,model):
    try:
        
            
        greek_result = model.transcribe(file_path,fp16=False,language='Greek')
        #print(f'Task completed with result: {greek_result}')
        logger.info(f'Speech to text task completed')
        update_greek_subs(post_id,greek_result,file_path)
        #create english subs 
        update_english_subs(post_id, greek_result, file_path)
        update_post_content(post_id, greek_result["text"])
        
        # Save `eng_text` to a temporary file for the next script
        temp_file = f"/tmp/{post_id}_greek_text.json"
        with open(temp_file, 'w') as f:
            json.dump({"greek_text": greek_result["text"]}, f)

    except Exception as e:
        logger.exception("Error in whisper_algorithm: %s")



if __name__ == '__main__':
    
    post_id = sys.argv[1]  
    file_path = sys.argv[2]

    whisper_model = whisper_load_model()
    english_text = whisper_algorithm(post_id, file_path, whisper_model)


