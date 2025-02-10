<?php
/*
Plugin Name: Create video or audio thumbnail
Description: A custom WordPress plugin for auto-creating thumbnails for uploaded videos or adding a default thumbnail for audio files.
*/

add_action('wp_insert_post', 'get_id_post', 10, 3);

function get_id_post($post_id, $post, $update) {
    if ($post->post_type === 'video' && $post->post_status === 'publish' && !$update) {
        global $stored_post_id;
        $stored_post_id = $post_id;
    }
}

add_action('forminator_form_after_save_entry', 'get_path', 10, 2);

function get_path($form_id, $response) {
    global $stored_post_id;

    if ($response && is_array($response)) {
        if ($response['success']) {
            if ($form_id == 39) {
                $entries = Forminator_API::get_entries($form_id);
                $entry = $entries[0];
                $meta_data = $entry->meta_data;

                // Retrieve the file URL
                $upload_file_path = $meta_data['upload-1']['value']['file']['file_path'];

                // Check if post ID and file path are available
                if ($stored_post_id && $upload_file_path) {
                    // Check file type (video or audio)
                    $mime_type = mime_content_type($upload_file_path);

                    if (strpos($mime_type, 'video') !== false) {
                        thumbnail_creator($stored_post_id, $upload_file_path);
                    } elseif (strpos($mime_type, 'audio') !== false) {
                        set_standard_thumbnail($stored_post_id);
                    }
                }
            }
        }
    }
}

function thumbnail_creator($post_id, $file_path) {
    $thumbnail_file = dirname($file_path) . '/' . basename($file_path, '.' . pathinfo($file_path, PATHINFO_EXTENSION)) . '-thumb.jpg';

    exec("ffmpeg -i " . escapeshellarg($file_path) . " -ss 00:00:02 -vframes 1 " . escapeshellarg($thumbnail_file));

    $filetype = wp_check_filetype(basename($thumbnail_file), null);
    $attachment = array(
        'guid' => $thumbnail_file,
        'post_mime_type' => $filetype['type'],
        'post_title' => preg_replace('/\.[^.]+$/', '', basename($thumbnail_file)),
        'post_content' => '',
        'post_status' => 'inherit'
    );

    $attach_id = wp_insert_attachment($attachment, $thumbnail_file, $post_id);
    wp_update_post(array('ID' => $attach_id, 'post_parent' => 0));

    set_post_thumbnail($post_id, $attach_id);
}

function set_standard_thumbnail($post_id) {
    $default_image_path = '/srv/www/wordpress/wp-content/uploads/forminator/39_acb3e86b40708b9b98b1088ed719b455/uploads/audio.png'; // Path to your default image
    error_log("File:" . $default_image_path);
    $filetype = wp_check_filetype(basename($default_image_path), null);

    $attachment = array(
        'guid' => $default_image_path,
        'post_mime_type' => $filetype['type'],
        'post_title' => 'Default Audio Thumbnail',
        'post_content' => '',
        'post_status' => 'inherit'
    );

    $attach_id = wp_insert_attachment($attachment, $default_image_path, $post_id);
    
     
    
    wp_update_post(array('ID' => $attach_id, 'post_parent' => 0));

    set_post_thumbnail($post_id, $attach_id);
    error_log("Default" . $post_id);
}
