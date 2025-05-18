<?php
/**
 * Plugin Name: Custom Video Search
 * Description: A plugin to add custom video search functionality.
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// Function to create the search form shortcode
function video_search_form_shortcode() {
    ob_start();
    ?>
    <form method="get" action="<?php echo esc_url(home_url('/')); ?>" onsubmit="return validateForm()">
        <input type="hidden" name="post_type" value="video">

        <div style="display: flex; flex-direction: column; gap: 10px;">
            <label for="topic">Choose a Topic to search in speech:</label>
            <select name="topic" id="topic">
                <option value="">--Select Topic--</option>
                <option value="event_name">Event Name</option>
                <option value="geopolitical_location">Geopolitical Location</option>
                <option value="location_name">Location Name</option>
                <option value="organization_name">Organization Name</option>
                <option value="person_name">Person Name</option>
                <option value="product_name">Product Name</option>
                <option value="search_all">Search Entire Speech Text</option>
            </select>

            <div id="input-container" style="display: flex; flex-direction: column;">
                <label for="topic_value">Enter Value:</label>
                <input type="text" name="topic_value" id="topic_value" required>
            </div>

            <p id="warning-message" style="color: red; display: none;">Please select a topic.</p>
        </div>

        <button type="submit">Search</button>
    </form>

    <script>
        function validateForm() {
            const topicSelect = document.getElementById('topic');
            const warningMessage = document.getElementById('warning-message');
            
            // Check if a topic is selected
            if (topicSelect.value === "") {
                warningMessage.style.display = "block";
                return false;
            } else {
                warningMessage.style.display = "none";
            }

            return true;
        }
    </script>
    <?php
    return ob_get_clean();
}

add_shortcode('video_search_form', 'video_search_form_shortcode');

// Function to customize the video search query
function custom_video_search_query($query) {
    if (!is_admin() && $query->is_main_query()) {
        if ($query->is_search() || (isset($_GET['post_type']) && $_GET['post_type'] === 'video')) {
            if (isset($_GET['topic']) && $_GET['topic'] === 'search_all') {
                $query->set('s', sanitize_text_field($_GET['topic_value']));
            } elseif (!empty($_GET['topic']) && !empty($_GET['topic_value'])) {
                $topic = sanitize_text_field($_GET['topic']);
                $topic_value = sanitize_text_field($_GET['topic_value']);

                $meta_query = array(
                    array(
                        'key'     => $topic,
                        'value'   => $topic_value,
                        'compare' => 'LIKE', // Allows partial matching
                    ),
                );

                $query->set('meta_query', $meta_query);
            }

            $query->set('post_type', 'video');
        }
    }
}

add_action('pre_get_posts', 'custom_video_search_query');
