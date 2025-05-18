<?php
/**
 * Video post entry layout
 *
 * @package OceanWP WordPress theme
 */




// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}


// Get post format.
$format = get_post_format();

// Blog style.
$style = get_theme_mod( 'ocean_blog_style', 'large-entry' );



// Quote format is completely different.
if ( 'quote' === $format ) {

	// Get quote entry content.
	get_template_part( 'partials/entry/quote' );

	return;

}

// If thumbnail style.
if ( 'thumbnail-entry' === $style ) {
	get_template_part( 'partials/entry/thumbnail-style/layout' );
} else {

	// Add classes to the blog entry post class.
	$classes = oceanwp_post_entry_classes(); ?>

	<article id="post-<?php the_ID(); ?>" <?php post_class( $classes ); ?>>

		<div class="blog-entry-inner clr">

			<?php
			// Get elements.
			$elements = oceanwp_blog_entry_elements_positioning();
			
			// Loop through elements.
			foreach ( $elements as $element ) {
				
			
				// Featured Image.
				if ( 'featured_image' === $element ) {

					// Get the post ID
					$post_id = get_the_ID();

					// Check if the post has a featured image
					if ( has_post_thumbnail( $post_id ) ) {
						// Display the featured image for the video post
						echo '<div class="video-featured-image">';
						echo get_the_post_thumbnail( $post_id, 'full' ); 
						echo '</div>';
					} else {
						// Display a placeholder or message if no featured image is set
						echo '<div class="no-featured-image">No Featured Image</div>';
					}
				}


				// Title.
				if ( 'title' === $element ) {

					get_template_part( 'partials/entry/header' );

				}

				// Meta.
				if ( 'meta' === $element ) {

					get_template_part( 'partials/entry/meta-video' );

				}

				// Content.
				if ( 'content' === $element ) {

					get_template_part( 'partials/entry/content' );

				}

				// Read more button.
				if ( 'read_more' === $element ) {

					get_template_part( 'partials/entry/readmore-video' );

				}
			}
			?>

			<?php
			$oe_disable_edit_post_active_status = get_option( 'oe_disable_edit_post_active_status', 'no' );
			if( $oe_disable_edit_post_active_status == 'no' ) {
				ocean_edit_post();
			}
			?>

		</div><!-- .blog-entry-inner -->

	</article><!-- #post-## -->

	<?php
}
?>

