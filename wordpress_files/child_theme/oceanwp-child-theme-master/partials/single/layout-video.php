<?php
/**
 * Single post layout
 *
 * @package OceanWP WordPress theme
 */

// Exit if accessed directly.
if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

?>

<article id="media-<?php the_ID(); ?>">

	<?php
	global $easywaveformplayer;
	$post_id = get_the_ID();
	$media_attachment_id = get_post_meta($post_id, 'upload-1', true);
	
	if ($media_attachment_id && !post_password_required()) :
		$path_info = pathinfo($media_attachment_id);
		$extension = strtolower($path_info['extension']); // Get file extension
		
		// Subtitles (only for video)
		$srt_file_path_gr = $path_info['dirname'] . '/' . $path_info['filename'] . '_el.vtt';
		$srt_file_path_en = $path_info['dirname'] . '/' . $path_info['filename'] . '_en.vtt';

		// Load JSON data from the file path
		$json_file_path = $path_info['dirname'] . '/' . $path_info['filename'] . '.json'; // Adjust this as necessary
		$json_data = json_decode(file_get_contents($json_file_path), true);
	

		// Extract FPS if it's included in the JSON
		$fps = isset($json_data['fps']) ? (float) $json_data['fps'] : 30; // Fallback to 30 if not available
		unset($json_data['fps']); // Remove FPS from JSON

		?>
		<style>
			.media-container {
				display: flex;
				align-items: flex-start;
				margin: 0;
				padding: 0;
			}

			video, audio {
				display: block;
				width: 640px;
				height: auto;
				margin-bottom: 0;
			}

			.action-sidebar {
				max-width: 200px;
				padding: 5px;
				border: 1px solid #ddd;
				border-radius: 5px;
				background-color: #f9f9f9;
				margin-left: 20px;
				text-align: center;
			}

			.action-button {
				display: block;
				width: 100%;
				margin-bottom: 5px;
				background-color: #0073aa;
				color: #fff;
				border: none;
				border-radius: 3px;
				padding: 10px;
				cursor: pointer;
				font-size: 14px;
			}

			.action-button:hover {
				background-color: #005177;
			}
			.audio-controls {
				display: flex;
				justify-content: center;
				margin-bottom: 15px; /* Adds spacing between button and waveform */
			}

			#playPauseButton {
				width: 60px;
				height: 60px;
				border: none;
				border-radius: 50%;
				background-color: #005177; /* Dark Blue */
				cursor: pointer;
				outline: none;
				box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
				display: flex;
				align-items: center;
				justify-content: center;
				position: relative;
				transition: all 0.3s ease-in-out;
			}

			#playPauseButton:hover {
				background-color: #0073aa; /* Medium Blue */
			}

			#playPauseButton.play-button::before {
				content: '';
				display: block;
				width: 0;
				height: 0;
				border-style: solid;
				border-width: 10px 0 10px 16px;
				border-color: transparent transparent transparent white;
				margin-left: 2px;
			}

			#playPauseButton.pause-button::before {
				content: '';
				display: block;
				width: 8px;
				height: 16px;
				background-color: white;
				position: absolute;
				left: 20px;
			}

			#playPauseButton.pause-button::after {
				content: '';
				display: block;
				width: 8px;
				height: 16px;
				background-color: white;
				position: absolute;
				right: 20px;
			}

			#waveform {
				border: 1px solid #ddd;
				border-radius: 5px;
				background-color: #eaf4fc; /* Light Blue Background */
				margin: 0 auto; /* Center waveform */
			}
		</style>

		<div class="media-container">
			<?php if ($extension === 'mp4') : ?>
				<!-- Video Player -->
				<figure id="videoContainer">
					<video id="mediaPlayer" width="640" height="360" controls autoplay preload="metadata">
						<source src="<?php echo esc_url($media_attachment_id); ?>" type="video/mp4" />
						<track kind="subtitles" src="<?php echo esc_url($srt_file_path_gr); ?>" srclang="gr" label="Greek" default />
						<track kind="subtitles" src="<?php echo esc_url($srt_file_path_en); ?>" srclang="en" label="English" />
						Your browser does not support the video tag.
					</video>
				</figure>
				
			<?php elseif (in_array($extension, ['mp3', 'wav', 'ogg'])) : ?>
				<div class="audio-controls">
    <button id="playPauseButton" class="play-button"></button>
</div>
<div id="waveform" style="width: 100%; height: 100px;"></div>

<script>
    document.addEventListener('DOMContentLoaded', function () {
        const waveform = WaveSurfer.create({
            container: '#waveform',
            waveColor: '#4a90e2', // Light Blue for the waveform
            progressColor: '#005177', // Dark Blue for progress
            height: 100,
            responsive: true,
            backend: 'mediaelement'
        });

        waveform.load('<?php echo esc_url($media_attachment_id); ?>');

        const playPauseButton = document.getElementById('playPauseButton');
        let isPlaying = false;

        playPauseButton.addEventListener('click', function () {
            waveform.playPause();
            isPlaying = !isPlaying;

            // Toggle button class for play/pause
            playPauseButton.classList.toggle('play-button', !isPlaying);
            playPauseButton.classList.toggle('pause-button', isPlaying);
        });
    });
</script>
			<?php else : ?>
				<p>Unsupported media format: <?php echo esc_html($extension); ?></p>
			<?php endif; ?>

			<!-- Sidebar with Action Buttons (only for video) -->
			<?php if ($extension === 'mp4' && $json_data): ?>
				<div class="action-sidebar">
					<h3>Actions</h3>
					<?php foreach ($json_data as $action => $frame): ?>
						<button class="action-button" data-frame="<?php echo esc_attr((int) $frame); ?>">
							<?php echo esc_html($action); ?>
						</button>
					<?php endforeach; ?>
				</div>
			<?php endif; ?>
		</div>

		<script>
			document.addEventListener('DOMContentLoaded', function() {
				const mediaPlayer = document.getElementById('mediaPlayer');
				const fps = <?php echo json_encode($fps); ?>;

				document.querySelectorAll('.action-button').forEach(button => {
					button.addEventListener('click', function(event) {
						event.preventDefault();

						const frame = parseInt(this.getAttribute('data-frame'), 10);
						const timestamp = frame / fps;

						if (mediaPlayer && !isNaN(timestamp)) {
							mediaPlayer.currentTime = timestamp;
							mediaPlayer.play();
						}
					});
				});
			});
		</script>
	<?php endif; ?>

</article>
	
	
	<?php
	// Get posts format.
	$format = get_post_format();
	
    
    
    
	// Get elements.
	$elements = oceanwp_blog_single_elements_positioning();
	
	// Loop through elements.
	foreach ( $elements as $element ) {

		

		// Title.
		if ( 'title' === $element ) {

			get_template_part( 'partials/single/header' );

		}

		// Meta.
		if ( 'meta' === $element ) {
			//error_log("The value of \$elements is: " . var_export($element, true));
			get_template_part( 'partials/single/meta-video' );

		}

		// Content.
		if ( 'content' === $element ) {

			get_template_part( 'partials/single/content' );

		}

		// Tags.
		if ( 'tags' === $element ) {
	
			get_template_part( 'partials/single/tags-video' );
		?>
			
    </li>
	<?php
	
			

			

		}

		// Social Share.
		if ( 'social_share' === $element
			&& OCEAN_EXTRA_ACTIVE ) {

			do_action( 'ocean_social_share' );

		}

		// Next/Prev.
		if ( 'next_prev' === $element ) {
			ob_start();
			get_template_part( 'partials/single/next-prev' );
			echo ob_get_clean();
		}

		// Author Box.
		if ( 'author_box' === $element ) {

			get_template_part( 'partials/single/author-bio' );

		}
		
		// Related Posts.
		if ( 'related_posts' === $element ) {
			ob_start();
			get_template_part( 'partials/single/related-posts' );
			echo ob_get_clean();
		}

		// Comments.
		if ( 'single_comments' === $element ) {
			ob_start();
			comments_template();
			echo ob_get_clean();
		}
	}
	
	?>

<?php

//Edit post shortcode
	
			// Check if the user is logged in
			if (is_user_logged_in()) {
				// Get the current user ID
				$current_user_id = get_current_user_id();

				// Get the post author ID
				$post_author_id = get_post_field('post_author', get_the_ID());

				// Check if the current user is the author of the post
				if ($current_user_id == $post_author_id) {
				
					//Edit post shortcode
					echo do_shortcode('[frontend_admin form=2638]');
				}
			}
			?>
</article>



