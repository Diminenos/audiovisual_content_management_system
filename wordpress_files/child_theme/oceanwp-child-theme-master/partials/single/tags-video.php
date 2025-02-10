<?php
/**
 * Blog single tags
 *
 * @package OceanWP WordPress theme
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

// Check if this is a 'video' post type and fetch the tags for 'video' custom taxonomy.
$post_type = get_post_type();




// Display the bookmark button
//echo do_shortcode('[oacsspl]');
?>

<div class="post-tags clr">
	

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

</div>
