<?php
/**
 * Search result page entry layout
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
?>


<article id="post-<?php the_ID(); ?>" <?php post_class( $classes ); ?>>

		<div class="blog-entry-inner clr">

			<?php
			// Get elements.
			$elements = oceanwp_blog_entry_elements_positioning();
			
			// Loop through elements.
			foreach ( $elements as $element ) {
				
				


				// Title.
				if ( 'title' === $element ) {

					get_template_part( 'partials/entry/header' );

				}

				// Meta.
				if ( 'meta' === $element ) {

					get_template_part( 'partials/entry/meta-video' );

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

?>

