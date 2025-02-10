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



/*

//prevent random letters when saving in forminator
function wpmudev_modify_uploaded_file_name( $filename, $ext, $dir, $unique_filename_callback, $alt_filenames, $number ) {	
	$uniq_id = substr($filename, 0, 12);
	if ( ctype_alnum( $uniq_id ) ) {
        $search = $uniq_id.'-';
		$filename = str_replace(  $search, '', $filename );
	}
	
    return $filename;
}

add_action( 'forminator_form_before_handle_submit', 'wpmudev_uploaded_filename_fix', 10, 1 );
add_action( 'forminator_form_before_save_entry', 'wpmudev_uploaded_filename_fix', 10, 1 );
function wpmudev_uploaded_filename_fix( $form_id ) {
	if ( $form_id != 39 ) { 
		return;
	}

	add_filter('wp_unique_filename', 'wpmudev_modify_uploaded_file_name', 10, 6);
}
*/

//Change button in post layout in page audiovisual content

//add_filter('ymc_post_read_more_2333_1', function () {
//    return 'Watch Video';
//}, 10, 1);

//function ymc_posts_selected($layouts, $founded_post) {
//    $layouts = 'Videos selected: ' . $founded_post .'';
//    return $layouts;
//}
//add_filter('ymc_posts_selected_2333_1', 'ymc_posts_selected', 10, 2);



// Function to hide widgets on video post pages
function my_post_layout_class($class) {
    // Check if we're on a video post page
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
    // Get the post ID from the AJAX request
    $post_id = intval($_POST['post_id']);
    if ($post_id) {
        // Output the edit post shortcode
        echo do_shortcode('[frontend_admin form=2638]');
    }
    wp_die(); // Required to terminate the AJAX request properly
}
add_action('wp_ajax_display_edit_post_form', 'ajax_display_edit_post_form');

//add thumbnail to user watchlist with the use of favorites plugin
function display_custom_favorites_with_thumbnails() {
    // Get the user's favorite posts (assuming Favorites plugin provides get_user_favorites function)
    $user_favorites = get_user_favorites();

    // Check if the user has any favorite posts
    if (empty($user_favorites)) {
        return '<p>No favorites added yet.</p>';
    }

    // Start output buffer to capture the HTML
    ob_start();

    echo '<div class="user-favorites" style="display: flex; flex-wrap: wrap; gap: 20px;">'; // Use flexbox for layout

    // Loop through each favorite post ID
    foreach ($user_favorites as $post_id) {
        // Retrieve the full post object using the ID
        $post = get_post($post_id);

        // Display post details if the post exists
        if ($post) {
            echo '<div class="favorite-post" style="flex: 0 0 150px; text-align: center;">'; // Adjust each item to be small
            echo '<h2 style="font-size: 16px;">' . esc_html(get_the_title($post_id)) . '</h2>';

            // Display a smaller featured image (using 'custom-small' size)
            if (has_post_thumbnail($post_id)) {
                echo '<div class="video-featured-image" style="max-width: 150px; margin: 0 auto;">';
                echo get_the_post_thumbnail($post_id, 'full'); // Custom size
                echo '</div>';
            } else {
                echo '<div class="no-featured-image" style="max-width: 150px; margin: 0 auto;">No Featured Image Available</div>';
            }

            // "Watch" link with bold text and larger font size
            echo '<a href="' . get_permalink($post_id) . '" style="font-weight: bold; font-size: 18px;">Watch</a>';

            echo '</div>';
        }
    }

    echo '</div>';

    // Return the output
    return ob_get_clean();
}
add_shortcode('custom_user_favorites', 'display_custom_favorites_with_thumbnails');

//for audio wave
function enqueue_wavesurfer_script() {
    wp_enqueue_script( 'wavesurfer', 'https://unpkg.com/wavesurfer.js', array(), null, true );
}
add_action( 'wp_enqueue_scripts', 'enqueue_wavesurfer_script' );