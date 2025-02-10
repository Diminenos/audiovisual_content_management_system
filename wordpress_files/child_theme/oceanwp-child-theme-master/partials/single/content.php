<?php
/**
 * Post single content
 *
 * @package OceanWP WordPress theme
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

?>

<?php do_action( 'ocean_before_single_post_content' ); ?>

<div class="entry-content clr"<?php oceanwp_schema_markup( 'entry_content' ); ?>>

    <button id="show-content-button" style="display: none;">Show Speech Content</button>
    <div id="actual-content" style="display: none;">
        <?php
        if ( empty( get_the_content() ) ) {
            echo '<p id="empty-content-message" style="display: block;">Speech content is not available.</p>';
        } else {
            the_content();
            wp_link_pages(
                array(
                    'before'      => '<div class="page-links">' . __( 'Pages:', 'oceanwp' ),
                    'after'       => '</div>',
                    'link_before' => '<span class="page-number">',
                    'link_after'  => '</span>',
                )
            );
        }
        ?>
    </div>
</div><!-- .entry -->

<?php do_action( 'ocean_after_single_post_content' ); ?>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        var showContentButton = document.getElementById('show-content-button');
        var actualContent = document.getElementById('actual-content');
        var emptyContentMessage = document.getElementById('empty-content-message');

        // Check if content is empty
        if (emptyContentMessage && actualContent && emptyContentMessage.style.display === 'block') {
            showContentButton.style.display = 'none';
        } else {
            // Content is not empty, show the button
            showContentButton.style.display = 'inline-block'; // Adjust the display property as needed
        }

        showContentButton.addEventListener('click', function () {
            if (emptyContentMessage && emptyContentMessage.style.display === 'block') {
                emptyContentMessage.style.display = 'none';
            }

            actualContent.style.display = (actualContent.style.display === 'none') ? 'block' : 'none';
        });
    });
</script>
