<?php
/**
 * Custom Search Results for Video Post Type
 */

get_header();

if ( have_posts() ) : ?>

    <header class="page-header">
        <h1 class="page-title">
            <?php printf( esc_html__( 'Search Results for: %s', 'your-theme-text-domain' ), '<span>' . get_search_query() . '</span>' ); ?>
        </h1>
    </header><!-- .page-header -->

    <div class="search-results-list">
        <?php
        // Start the Loop.
        while ( have_posts() ) :
            the_post();

            // Check if the post type is 'video'
            if ( 'video' === get_post_type() ) : ?>

                <article id="post-<?php the_ID(); ?>" <?php post_class(); ?>>
                    <header class="entry-header">
                        <h2 class="entry-title">
                            <a href="<?php the_permalink(); ?>" rel="bookmark"><?php the_title(); ?></a>
                        </h2>
                    </header><!-- .entry-header -->

                    <div class="entry-content">
                        <?php
                        // Display the excerpt or summary of the post
                        the_excerpt();

                        // Display custom fields using ACF
                        $geopolitical_location = get_field('geopolitical_location');
                        $event_name = get_field('event_name');
                        $date_value = get_field('date_value');
                        $person_name = get_field('person_name');
                        $organization_name = get_field('organization_name');

                        // Display custom field values
                        if ($geopolitical_location) {
                            echo '<p><strong>Geopolitical Location:</strong> ' . esc_html($geopolitical_location) . '</p>';
                        }
                        if ($event_name) {
                            echo '<p><strong>Event Name:</strong> ' . esc_html($event_name) . '</p>';
                        }
                        if ($date_value) {
                            echo '<p><strong>Date:</strong> ' . esc_html($date_value) . '</p>';
                        }
                        if ($person_name) {
                            echo '<p><strong>Person Name:</strong> ' . esc_html($person_name) . '</p>';
                        }
                        if ($organization_name) {
                            echo '<p><strong>Organization Name:</strong> ' . esc_html($organization_name) . '</p>';
                        }
                        ?>
                    </div><!-- .entry-content -->
                </article><!-- #post-## -->

            <?php endif;

        endwhile;

        // Pagination
        the_posts_pagination();

    else :

        // If no content, include the "No posts found" template.
        get_template_part( 'template-parts/content', 'none' );

    endif;
    ?>
</div>

<?php get_footer(); ?>