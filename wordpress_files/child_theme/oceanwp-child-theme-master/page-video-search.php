<?php
/**
 * The template for displaying search forms.
 *
 * @package OceanWP WordPress theme
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}
get_header(); 
// Post type.
$search_post_type = get_theme_mod( 'ocean_menu_search_source', 'video' );

// Generate unique form ID.
$ocean_sf_id = oceanwp_unique_id( 'ocean-search-form-' );

?><form method="get" action="<?php echo esc_url(home_url('/')); ?>" style="max-width: 500px; margin: 0 auto;"> <!-- Adjust the width as necessary -->

<input type="hidden" name="post_type" value="video">

<!-- Container for dropdown and input field -->
<div style="display: flex; flex-direction: column; gap: 10px;">

    <!-- Dropdown for selecting the topic -->
    <label for="topic">Choose a Topic:</label>
    <select name="topic" id="topic" style="padding: 10px; border-radius: 4px; border: 1px solid #ccc;">
        <option value="">--Select Topic--</option>
        <option value="event_name">Event Name</option>
        <option value="building_name">Building Name</option>
        <option value="geopolitical_location">Geopolitical Location</option>
        <option value="language_name">Language Name</option>
        <option value="law_name">Law Name</option>
        <option value="location_name">Location Name</option>
        <option value="money_name">Money Name</option>
        <option value="affiliation">Affiliation</option>
        <option value="organization_name">Organization Name</option>
        <option value="person_name">Person Name</option>
        <option value="product_name">Product Name</option>
        <option value="name_of_work_of_art">Name of Work of Art</option>
        <option value="search_all">Search Entire Speech Text</option> <!-- New option for full content search -->
    </select>

    <!-- Input field for value -->
    <div id="input-container" style="display: flex; flex-direction: column;">
        <label for="topic_value">Enter Value:</label>
        <input type="text" name="topic_value" id="topic_value" style="padding: 10px; border-radius: 4px; border: 1px solid #ccc;">
    </div>

</div>

<button type="submit" style="margin-top: 10px; padding: 10px 20px; border-radius: 4px; background-color: #333; color: white; border: none;">Search</button>
</form>