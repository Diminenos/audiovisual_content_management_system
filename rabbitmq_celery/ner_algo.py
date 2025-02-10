import spacy
from video_updates import save_custom_fields_to_wordpress
import logging
import logger_config
import sys
import json
from googletrans import Translator  # Assuming you use Google Translate for translation
 
# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)

def create_topic_from_texts(post_id, file_path, text):
    try:
        # Load the NER model
        nlp = spacy.load('el_core_news_lg')
        translator = Translator()  # Initialize the translator

    except Exception as e:
        logger.exception(f"Error loading NER model or translator: {e}")
        return

    try:
        # Chunking the input text to avoid memory issues
        max_chunk_size = 1000  
        chunks = [text[i:i + max_chunk_size] for i in range(0, len(text), max_chunk_size)]

        # Prepare the data to save as custom fields in WordPress
        acf_fields = {
            'organization_name': [],
            'product_name': [],
            'person_name': [],
            'event_name': [],
            'geopolitical_location': [],
            'location_name': [],
        }

        # Process Greek text
        for chunk in chunks:
            doc = nlp(chunk)
            for entity in doc.ents:
                label = entity.label_.lower()
                entity_text = entity.text

                # Add the Greek entities to the fields
                if label == 'org':
                    acf_fields['organization_name'].append(entity_text)
                elif label == 'product':
                    acf_fields['product_name'].append(entity_text)
                elif label == 'person':
                    acf_fields['person_name'].append(entity_text)
                elif label == 'event':
                    acf_fields['event_name'].append(entity_text)
                elif label == 'gpe':
                    acf_fields['geopolitical_location'].append(entity_text)
                elif label == 'loc':
                    acf_fields['location_name'].append(entity_text)

        # Translate the named entities to English
        translated_acf_fields = {
            'organization_name': [],
            'product_name': [],
            'person_name': [],
            'event_name': [],
            'geopolitical_location': [],
            'location_name': [],
        }

        for key, values in acf_fields.items():
            for value in values:
                try:
                    # Translate each entity
                    translated_entity = translator.translate(value, src='el', dest='en').text
                    translated_acf_fields[key].append(translated_entity)
                except Exception as e:
                    logger.error(f"Error translating entity '{value}': {e}")

        # Remove duplicates 
        for key in acf_fields:
            acf_fields[key] = list(set(acf_fields[key]))  
            translated_acf_fields[key] = list(set(translated_acf_fields[key]))  

        # Combine both Greek and English fields into one dictionary
        combined_acf_fields = {
            'organization_name': acf_fields['organization_name'] + translated_acf_fields['organization_name'],
            'product_name': acf_fields['product_name'] + translated_acf_fields['product_name'],
            'person_name': acf_fields['person_name'] + translated_acf_fields['person_name'],
            'event_name': acf_fields['event_name'] + translated_acf_fields['event_name'],
            'geopolitical_location': acf_fields['geopolitical_location'] + translated_acf_fields['geopolitical_location'],
            'location_name': acf_fields['location_name'] + translated_acf_fields['location_name'],
        }

        # Save the custom fields to WordPress
        save_custom_fields_to_wordpress(post_id, combined_acf_fields)

    except Exception as e:
        logger.exception(f"Error processing text or saving custom fields: {e}")
    
    
if __name__ == '__main__':
    post_id = sys.argv[1]  
    file_path = sys.argv[2]
    # Load `eng_text` from the temporary file
    temp_file = f"/tmp/{post_id}_greek_text.json"
    with open(temp_file, 'r') as f:
        text = json.load(f)["greek_text"]

    create_topic_from_texts(post_id, file_path, text)


