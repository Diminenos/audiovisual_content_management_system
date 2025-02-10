import requests
from requests.auth import HTTPBasicAuth
import logging
import logger_config
from datetime import timedelta, datetime
import os 
import json
from googletrans import Translator
from dotenv import load_dotenv

# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)




#Update audio classification tags

def update_audio_tag(post_id, tag_names):
    # Define your custom taxonomy for tags
    custom_taxonomy = 'audio-classification-tag' 
    # Load the .env file
    # Load the .env file
    load_dotenv('/home/dimineno/consumer_celery/wordpress_credential.env')

    # Access the variables
    wordpress_url = os.getenv('WORDPRESS_URL')
    username = os.getenv('WORDPRESS_USERNAME')
    app_password = os.getenv('WORDPRESS_APP_PASSWORD')
   

    try:
        # Step 1: Get existing terms for the custom taxonomy
        response = requests.get(f"{wordpress_url}/{custom_taxonomy}", auth=HTTPBasicAuth(username, app_password))
        response.raise_for_status()
        existing_terms = {term['slug']: term['id'] for term in response.json()}  # Dict of existing terms

        # Step 2: Get existing tags for the post
        post_response = requests.get(f"{wordpress_url}/video/{post_id}", auth=HTTPBasicAuth(username, app_password))
        post_response.raise_for_status()
        post_data = post_response.json()
        existing_tag_ids = set(post_data.get('audio-classification-tag', []))

        # Step 3: Prepare the term IDs to associate with the post (merge with existing)
        tag_ids = list(existing_tag_ids)  # Start with existing tags

        for tag in tag_names:
            tag_slug = tag.lower().replace(" ", "-")  # Slugify the tag name

            if tag_slug not in existing_terms:
                # Create new term if it doesn't exist
                data = {'name': tag, 'slug': tag_slug}
                create_response = requests.post(f"{wordpress_url}/{custom_taxonomy}", json=data, auth=HTTPBasicAuth(username, app_password))
                
                if create_response.status_code == 400 and create_response.json().get('code') == "term_exists":
                    # If term already exists, get the term ID from the error response
                    existing_term_id = create_response.json()['data']['term_id']
                    if existing_term_id not in tag_ids:
                        tag_ids.append(existing_term_id)
                        logger.info(f"Term '{tag}' already exists. Added existing term ID.")
                elif create_response.status_code in [201, 200]:
                    new_term = create_response.json()
                    tag_ids.append(new_term['id'])
                    logger.info(f"Term '{tag}' added successfully.")
                else:
                    logger.error(f"Failed to add term '{tag}': {create_response.content.decode()}")
            else:
                # If the term exists in our existing_terms dictionary, use its ID
                term_id = existing_terms[tag_slug]
                if term_id not in tag_ids:
                    tag_ids.append(term_id)
                    logger.info(f"Term '{tag}' already exists in existing terms.")


        # Step 4: Update the post with the combined tag IDs
        update_post_response = requests.post(f"{wordpress_url}/video/{post_id}", json={"audio-classification-tag": tag_ids}, auth=HTTPBasicAuth(username, app_password))

        if update_post_response.status_code in [200, 201]:
            logger.info(f"Post {post_id} updated successfully with tags.")
        else:
            logger.error(f"Failed to update post {post_id}: {update_post_response.content.decode()}")

    except requests.exceptions.RequestException as e:
        logger.exception(f"HTTP error updating post content for custom post type: {e}")

    except Exception as e:
        logger.exception(f"Unexpected error updating post content for custom post type: {e}")

#Update action recongition tags

def update_action_tag(post_id, tag_names):
    # Define your custom taxonomy for tags
    custom_taxonomy = 'action-recognition-tag'
    # Load the .env file
    # Load the .env file
    load_dotenv('/home/dimineno/consumer_celery/wordpress_credential.env')

    # Access the variables
    wordpress_url = os.getenv('WORDPRESS_URL')
    username = os.getenv('WORDPRESS_USERNAME')
    app_password = os.getenv('WORDPRESS_APP_PASSWORD')
   

    try:
        # Step 1: Get existing terms for the custom taxonomy
        response = requests.get(f"{wordpress_url}/{custom_taxonomy}", auth=HTTPBasicAuth(username, app_password))
        response.raise_for_status()
        existing_terms = {term['slug']: term['id'] for term in response.json()}  # Dict of existing terms

        # Step 2: Get existing tags for the post
        post_response = requests.get(f"{wordpress_url}/video/{post_id}", auth=HTTPBasicAuth(username, app_password))
        post_response.raise_for_status()
        post_data = post_response.json()
        existing_tag_ids = set(post_data.get('action-recognition-tag', []))

        # Step 3: Prepare the term IDs to associate with the post (merge with existing)
        tag_ids = list(existing_tag_ids)  # Start with existing tags

        for tag in tag_names:
            tag_slug = tag.lower().replace(" ", "-")  # Slugify the tag name

            if tag_slug not in existing_terms:
                # Create new term if it doesn't exist
                data = {'name': tag, 'slug': tag_slug}
                create_response = requests.post(f"{wordpress_url}/{custom_taxonomy}", json=data, auth=HTTPBasicAuth(username, app_password))
                
                if create_response.status_code == 400 and create_response.json().get('code') == "term_exists":
                    # If term already exists, get the term ID from the error response
                    existing_term_id = create_response.json()['data']['term_id']
                    if existing_term_id not in tag_ids:
                        tag_ids.append(existing_term_id)
                        logger.info(f"Term '{tag}' already exists. Added existing term ID.")
                elif create_response.status_code in [201, 200]:
                    new_term = create_response.json()
                    tag_ids.append(new_term['id'])
                    logger.info(f"Term '{tag}' added successfully.")
                else:
                    logger.error(f"Failed to add term '{tag}': {create_response.content.decode()}")
            else:
                # If the term exists in our existing_terms dictionary, use its ID
                term_id = existing_terms[tag_slug]
                if term_id not in tag_ids:
                    tag_ids.append(term_id)
                    logger.info(f"Term '{tag}' already exists in existing terms.")


        # Step 4: Update the post with the combined tag IDs
        update_post_response = requests.post(f"{wordpress_url}/video/{post_id}", json={"action-recognition-tag": tag_ids}, auth=HTTPBasicAuth(username, app_password))

        if update_post_response.status_code in [200, 201]:
            logger.info(f"Post {post_id} updated successfully with tags.")
        else:
            logger.error(f"Failed to update post {post_id}: {update_post_response.content.decode()}")

    except requests.exceptions.RequestException as e:
        logger.exception(f"HTTP error updating post content for custom post type: {e}")

    except Exception as e:
        logger.exception(f"Unexpected error updating post content for custom post type: {e}")


#Update greek subs

def update_greek_subs(post_id,subs,file_path):

 
    try:
        
        #Replace the domain part with the local server path.
        subs_path = os.path.splitext(file_path)[0] + '_el.vtt'
        
        # Open the file in write mode
        with open(subs_path, "w", encoding="utf-8") as vtt_file:
            
            vtt_file.write("WEBVTT\n\n")

            subtitle_index = 1  
            segments = subs['segments']

            # Iterate over the segments
            for segment in segments:
                start_time = timedelta(seconds=segment['start'])
                end_time = timedelta(seconds=segment['end'])
                segment_text = segment['text']

                # Convert timedelta to datetime to use strftime
                start_datetime = datetime(1, 1, 1) + start_time
                end_datetime = datetime(1, 1, 1) + end_time

                # Format the timestamp in MM:SS.SSS
                start_timestamp = start_datetime.strftime('%M:%S.%f')[:-3]
                end_timestamp = end_datetime.strftime('%M:%S.%f')[:-3]

                # Write the subtitle  timestamp, and text to the VTT file
                vtt_file.write(f"{start_timestamp} --> {end_timestamp}\n")
                vtt_file.write(f"{segment_text}\n\n")

                # Increment the subtitle index for the next iteration
                subtitle_index += 1
        
        logger.info(f'Greek subs uploaded')
        

    except Exception as e:
        # Handle any exceptions that occur during the update process
        logger.exception(f"Error uploading greek subs: {e}")


#Create english subs 

def update_english_subs(post_id,subs,file_path):

 
    try:
        
        # Translator initialization
        translator = Translator()

        # Replace the domain part with the local server path.
        subs_path = os.path.splitext(file_path)[0] + '_en.vtt'
        #full_english_text = ""

        # Open the file in write mode for both VTT and full English text
        with open(subs_path, "w", encoding="utf-8") as vtt_file:

            vtt_file.write("WEBVTT\n\n")

            subtitle_index = 1
            segments = subs['segments']

            # Iterate over the segments
            for segment in segments:
                start_time = timedelta(seconds=segment['start'])
                end_time = timedelta(seconds=segment['end'])
                greek_text = segment['text']

                # Translate Greek text to English
                english_text = translator.translate(greek_text, src='el', dest='en').text

                # Convert timedelta to datetime to use strftime
                start_datetime = datetime(1, 1, 1) + start_time
                end_datetime = datetime(1, 1, 1) + end_time

                # Format the timestamp in MM:SS.SSS
                start_timestamp = start_datetime.strftime('%M:%S.%f')[:-3]
                end_timestamp = end_datetime.strftime('%M:%S.%f')[:-3]

                # Write the subtitle timestamp and English text to the VTT file
                vtt_file.write(f"{start_timestamp} --> {end_timestamp}\n")
                vtt_file.write(f"{english_text}\n\n")

                # Append the English text to the full text variable
                #full_english_text += f"{english_text} "

                # Increment the subtitle index for the next iteration
                subtitle_index += 1

        
            
        logger.info(f'English subs uploaded')
        #return full_english_text     

    except Exception as e:
        # Handle any exceptions that occur during the update process
        logger.exception(f"Error uploading english subs: {e}")

#update video content
def update_post_content(post_id, new_content):
    

    try:
        # Load the .env file
        load_dotenv('/home/dimineno/consumer_celery/wordpress_credential.env')
        # Access the variables
        wordpress_url = os.getenv('WORDPRESS_URL')
        username = os.getenv('WORDPRESS_USERNAME')
        app_password = os.getenv('WORDPRESS_APP_PASSWORD')
        # Prepare the data to send (only updating the content)
        updated_content = {'content': new_content}

        # Make the request to update the post content
        response = requests.post(
            f'{wordpress_url}/video/{post_id}',
            json=updated_content,
            auth=HTTPBasicAuth(username, app_password)
        )

        # Check the response and log the result
        if response.status_code == 200:
            logger.info(f"Video {post_id} content updated successfully!")
        else:
            # Properly format error logging with a single string
            logger.error(f"Failed to update post content: {response.status_code}. Details: {response.text}")

    except Exception as e:
        # Handle any exceptions that occur during the update process
        logger.exception(f"Error updating the content: {e}")


#Update the custom video fields from ner algo
def save_custom_fields_to_wordpress(post_id, acf_fields):
    try:
        # Load the .env file
        load_dotenv('/home/dimineno/consumer_celery/wordpress_credential.env')
        # Access the variables
        wordpress_url = os.getenv('WORDPRESS_URL')
        username = os.getenv('WORDPRESS_USERNAME')
        app_password = os.getenv('WORDPRESS_APP_PASSWORD')

        url = f"{wordpress_url}/video/{post_id}"  # Adjust the endpoint for your custom post type
        headers = {
            'Authorization': f'Bearer {app_password}',  # Use basic auth here
            'Content-Type': 'application/json'
        }

        # Prepare data to save as custom fields
        data = {
            'acf': {}
        }

        # Add custom fields to the data dictionary
        for key, values in acf_fields.items():
            if values:  # Only save fields that have values
                data['acf'][key] = ', '.join(values)  # Store as comma-separated values

        # Send the request to update the post
        response = requests.post(url, json=data, auth=HTTPBasicAuth(username, app_password))

        # Logging the request for debugging purposes
        #print("Request URL:", url)
        #print("Request Data:", data)

        # Check the response
        if response.status_code == 200:
            logger.info("Custom fields saved successfully.")
        else:
            logger.error(f"Failed to save custom fields: {response.status_code}, {response.text}")
    
    except requests.exceptions.RequestException as req_err:
        logger.exception(f"Request error occurred: {req_err}")
    except json.JSONDecodeError as json_err:
        logger.exception(f"JSON encoding error occurred: {json_err}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")




def update_content_type(post_id, is_audio):
    try:
        load_dotenv('/home/dimineno/consumer_celery/wordpress_credential.env')
        # Access the variables
        wordpress_url = os.getenv('WORDPRESS_URL')
        username = os.getenv('WORDPRESS_USERNAME')
        app_password = os.getenv('WORDPRESS_APP_PASSWORD')

        url = f"{wordpress_url}/video/{post_id}"  # Adjust for your custom post type
        
        # Use the known term IDs
        term_id = 398 if is_audio else 399
        
        # Set up the payload for updating the taxonomy
        payload = {
            "content_type": [term_id]  # Use the term ID directly
        }

        # Send the request to update the post
        response = requests.put(url, json=payload, auth=HTTPBasicAuth(username, app_password))

        # Debugging logs
        logger.debug(f"Request URL: {url}")
        logger.debug(f"Request Payload: {payload}")

        # Check the response
        if response.status_code == 200:
            logger.info("Content type updated successfully.")
        else:
            logger.error(f"Failed to update content type: {response.status_code}, {response.text}")
    
    except requests.exceptions.RequestException as req_err:
        logger.exception(f"Request error occurred: {req_err}")
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
