<?php
/**
 * OceanWP Child Theme Functions
 *
 * When running a child theme (see http://codex.wordpress.org/Theme_Development
 * and http://codex.wordpress.org/Child_Themes), you can override certain
 * functions (those wrapped in a function_exists() call) by defining them first
 * in your child theme's functions.php file. The child theme's functions.php
 * file is included before the parent theme's file, so the child theme
 * functions will be used.
 *
 * Text Domain: oceanwp
 * @link http://codex.wordpress.org/Plugin_API
 *
 */

/**
 * Load the parent style.css file
 *
 * @link http://codex.wordpress.org/Child_Themes
 */
function oceanwp_child_enqueue_parent_style() {

	// Dynamically get version number of the parent stylesheet (lets browsers re-cache your stylesheet when you update the theme).
	$theme   = wp_get_theme( 'OceanWP' );
	$version = $theme->get( 'Version' );

	// Load the stylesheet.
	wp_enqueue_style( 'child-style', get_stylesheet_directory_uri() . '/style.css', array( 'oceanwp-style' ), $version );
	
}

add_action( 'wp_enqueue_scripts', 'oceanwp_child_enqueue_parent_style' );



function oceanwp_metabox( $types ) {

	// Your custom post type
	$types[] = 'video';

	// Return
	return $types;

}
add_filter( 'ocean_main_metaboxes_post_types', 'oceanwp_metabox', 20 );




// Function to hide widgets on video post pages
function my_post_layout_class($class) {
    
    if (is_singular('video') || is_page()) {
        $class='full-width';
    }
	return $class;
	
}
add_filter('ocean_post_layout_class', 'my_post_layout_class',20);



//In user profile display custom post type video 
 
function custom_um_profile_query_make_posts( $args = array() ) 
{
    $args['post_type'] = 'video';
 
    return $args;
}
 
// call your function using the UM hook

add_filter( 'um_profile_query_make_posts', 'custom_um_profile_query_make_posts', 12, 1 );
 

//add button to edit video in single post page
function ajax_display_edit_post_form() {
    
    $post_id = intval($_POST['post_id']);
    if ($post_id) {
        
        echo do_shortcode('[frontend_admin form=2638]');
    }
    wp_die(); 
}
add_action('wp_ajax_display_edit_post_form', 'ajax_display_edit_post_form');

//add thumbnail to user watchlist with the use of favorites plugin
function display_custom_favorites_with_thumbnails() {
    
    $user_favorites = get_user_favorites();

 
    if (empty($user_favorites)) {
        return '<p>No favorites added yet.</p>';
    }

    
    ob_start();

    echo '<div class="user-favorites" style="display: flex; flex-wrap: wrap; gap: 20px;">'; 

    
    foreach ($user_favorites as $post_id) {
        
        $post = get_post($post_id);

     
        if ($post) {
            echo '<div class="favorite-post" style="flex: 0 0 150px; text-align: center;">'; 
            echo '<h2 style="font-size: 16px;">' . esc_html(get_the_title($post_id)) . '</h2>';

           
            if (has_post_thumbnail($post_id)) {
                echo '<div class="video-featured-image" style="max-width: 150px; margin: 0 auto;">';
                echo get_the_post_thumbnail($post_id, 'full'); 
                echo '</div>';
            } else {
                echo '<div class="no-featured-image" style="max-width: 150px; margin: 0 auto;">No Featured Image Available</div>';
            }

            
            echo '<a href="' . get_permalink($post_id) . '" style="font-weight: bold; font-size: 18px;">Watch</a>';

            echo '</div>';
        }
    }

    echo '</div>';

   
    return ob_get_clean();
}
add_shortcode('custom_user_favorites', 'display_custom_favorites_with_thumbnails');

//for audio wave
function enqueue_wavesurfer_script() {
    wp_enqueue_script( 'wavesurfer', 'https://unpkg.com/wavesurfer.js', array(), null, true );
}
add_action( 'wp_enqueue_scripts', 'enqueue_wavesurfer_script' );