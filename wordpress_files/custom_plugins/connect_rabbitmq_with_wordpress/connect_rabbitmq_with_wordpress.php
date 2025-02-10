<?php
/*
Plugin Name: Connect RabbitMQ with wordpress
Description: A custom WordPress plugin for sending posts to RabbitMQ.
*/


require_once('/srv/www/wordpress/wp-load.php');
require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage; 







function send_to_rabbitmq($post_id, $file_path) { 
    $connection = new AMQPStreamConnection(
        'localhost', // RabbitMQ host
        5672, // RabbitMQ port
        '*****', // RabbitMQ username
        '*****', // RabbitMQ password
        '*****' //Vhost
    );
    
    
    //Set up connection
    //Create separate channels for each queue
    $channel1 = $connection->channel();
    $channel1->confirm_select();
    
    
    //Declare the exchanges and queues for each channel
    $channel1->exchange_declare('algo_exchange', 'fanout', True, True, false);
    
    //Message data for eacch channel

    $message_body = array(
        'file_path' => $file_path,
        'post_id' => $post_id
    );

    // Convert the array to a JSON string
    $message_json = json_encode($message_body);

    $messageProperties=['delivery_mode' => 2];
    //create and send messages to each queue
    $message1 = new AmqpMessage($message_json,$messageProperties);
   

    // Publish the message to the exchange
    $channel1->basic_publish($message1, 'algo_exchange');

    // Close the channel and connection
    $channel1->close();
 
    $connection->close();

}


add_action('wp_insert_post', 'get_post_id', 10, 3);

function get_post_id($post_id, $post,$update) {
    if ($post->post_type === 'video' && $post->post_status === 'publish' && !$update) {
    
        global $stored_post_id;
        $stored_post_id = $post_id;      
                //error_log("The valuessssssss of \$submitted_data is: " . var_export($submitted_data, true));
                //if (isset($meta_data['upload-1']['value']['file']['file_url']) && isset($meta_data['postdata-1']['value']['postdata']['value']['post-title'])) {
                    //Retrieve post id
                    //$post_id=$meta_data['postdata-1']['value']['postdata']['value']['postdata'];
                    
        //error_log("The valuessssssss of \$stored_post_id is: " . var_export($stored_post_id, true));
   }    

}
add_action('forminator_form_after_save_entry', 'get_file_path', 10, 2);
         
function get_file_path($form_id,$response) {
    // Retrieve the stored post ID
    global $stored_post_id;
    if ($response && is_array($response)){
        if ($response['success']){
            if ($form_id == 39){
                $entries = Forminator_API::get_entries( $form_id );
                $entry=$entries[0];
                $meta_data = $entry->meta_data;
                // Retrieve the file URL
                $upload_file_path = $meta_data['upload-1']['value']['file']['file_path'];
                //error_log("The valuessssssss of \$upload_file_path is: " . var_export($upload_file_path, true));

            }
        }
    }
    // Check if both post ID and file path are available
    if ($stored_post_id && $upload_file_path) {
        // Send the values via RabbitMQ or perform any desired action
        send_to_rabbitmq($stored_post_id, $upload_file_path);
    }
}

