<?php
/*
Plugin Name: My videos display
Description: A custom WordPress plugin for displaying only the video of the logged in user

*/



function filter_posts_by_author( $query ) {


   if ( is_page(array('my-content')) && is_user_logged_in() ) {
	 
	 $user_id=get_current_user_id();
	 $query->set('author', $user_id);
         
   }
   
}
add_action('powerpack/query/custom','filter_posts_by_author',10,2 );


//,
