<?php
/**
 * The default template for displaying post meta.
 *
 * @package OceanWP WordPress theme
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Get meta sections.
$sections = oceanwp_blog_entry_meta();

// Return if sections are empty.
if ( empty( $sections ) ) {
	return;
}

// Get meta separator style.
$meta_class = oceanwp_theme_blog_meta_separator();

do_action( 'ocean_before_blog_entry_meta' );
?>

<ul class="meta obem-<?php echo $meta_class; ?> clr" aria-label="<?php esc_attr_e( 'Post details:', 'oceanwp' ); ?>">

	<?php
	// Loop through meta sections.
	foreach ( $sections as $section ) {
		?>

		<?php if ( 'author' === $section ) { ?>
			<li class="meta-author"<?php oceanwp_schema_markup( 'author_name' ); ?>><span class="screen-reader-text"><?php esc_html_e( 'Post author:', 'oceanwp' ); ?></span><?php oceanwp_icon( 'user' ); ?><?php echo esc_html( the_author_posts_link() ); ?></li>
		<?php } ?>

		<?php if ( 'date' === $section ) { ?>
			<li class="meta-date"<?php oceanwp_schema_markup( 'publish_date' ); ?>><span class="screen-reader-text"><?php esc_html_e( 'Post published:', 'oceanwp' ); ?></span><?php oceanwp_icon( 'date' ); ?><?php echo get_the_date(); ?></li>
		<?php } ?>

		<?php if ( 'mod-date' === $section ) { ?>
			<li class="meta-mod-date"<?php oceanwp_schema_markup( 'modified_date' ); ?>><span class="screen-reader-text"><?php esc_html_e( 'Post last modified:', 'oceanwp' ); ?></span><?php oceanwp_icon( 'm_date' ); ?><?php echo esc_html( get_the_modified_date() ); ?></li>
		<?php } ?>

		<?php if ( 'categories' === $section ) : ?>
    <li class="meta-cat">
        <span class="screen-reader-text"><?php esc_html_e( 'Post category:', 'oceanwp' ); ?></span>
        <?php oceanwp_icon( 'category' ); ?>
        <?php
        // Get the current post ID
        $post_id = get_the_ID();
        
        // Fetch the post type
        $post_type = get_post_type( $post_id );
        
        $terms = get_the_terms( $post_id, 'video-category' ); // Custom taxonomy 'video_category'
        

        // Check if any terms were retrieved
        if ( ! empty( $terms ) && ! is_wp_error( $terms ) ) {
            // Loop through the terms and display them
            foreach ( $terms as $term ) {
                echo '<a href="' . esc_url( get_term_link( $term ) ) . '">' . esc_html( $term->name ) . '</a>';
                echo '<span class="owp-sep" aria-hidden="true"></span>';
            }
        } else {
            // Display a message if no categories were found
            echo '<span>No categories found.</span>';
        }
        ?>
    </li>
	<?php
    // Fetch the terms for the audio-classification-tag and action-classification-tag taxonomies
    $audio_tags = get_the_terms( get_the_ID(), 'audio-classification-tag' );
    $action_tags = get_the_terms( get_the_ID(), 'action-recognition-tag' ); 
?>
<li class="meta-tags">
    <!-- Audio Tags -->
    <div class="meta-tags-audio">
        <span class="owp-tag-text"><i class="fas fa-volume-up"></i></span>
        <?php if ( $audio_tags && ! is_wp_error( $audio_tags ) ) : ?>
            <?php
            $audio_output = [];
            foreach ( $audio_tags as $tag ) {
                $audio_output[] = '<a href="' . get_term_link( $tag ) . '">' . esc_html( $tag->name ) . '</a>';
            }
            echo implode( '<span class="owp-sep">,</span> ', $audio_output );
            ?>
        <?php else : ?>
            <?php echo esc_html__( 'No Audio Tags', 'oceanwp' ); ?>
        <?php endif; ?>
    </div>

    <!-- Action Tags -->
    <div class="meta-tags-action">
        <span class="owp-tag-text"><i class="fas fa-bolt"></i></span>
        <?php if ( $action_tags && ! is_wp_error( $action_tags ) ) : ?>
            <?php
            $action_output = [];
            foreach ( $action_tags as $tag ) {
                $action_output[] = '<a href="' . get_term_link( $tag ) . '">' . esc_html( $tag->name ) . '</a>';
            }
            echo implode( '<span class="owp-sep">,</span> ', $action_output );
            ?>
        <?php else : ?>
            <?php echo esc_html__( 'No Action Tags', 'oceanwp' ); ?>
        <?php endif; ?>
    </div>
</li>


		<?php if ( 'reading-time' === $section ) { ?>
			<li class="meta-cat"><span class="screen-reader-text"><?php esc_html_e( 'Reading time:', 'oceanwp' ); ?></span><?php oceanwp_icon( 'r_time' ); ?><?php echo esc_html( ocean_reading_time() ); ?></li>
		<?php } ?>

		<?php if ( 'comments' === $section && comments_open() && ! post_password_required() ) { ?>
			<li class="meta-comments"><span class="screen-reader-text"><?php esc_html_e( 'Post comments:', 'oceanwp' ); ?></span><?php oceanwp_icon( 'comment' ); ?><?php comments_popup_link( esc_html__( '0 Comments', 'oceanwp' ), esc_html__( '1 Comment', 'oceanwp' ), esc_html__( '% Comments', 'oceanwp' ), 'comments-link' ); ?></li>
		<?php } ?>
		<?php endif; ?>
	<?php } ?>

</ul>

<?php do_action( 'ocean_after_blog_entry_meta' ); ?>
