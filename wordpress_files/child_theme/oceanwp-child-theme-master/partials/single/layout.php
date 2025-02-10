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

<article id="post-<?php the_ID(); ?>">

	<?php
	$post_id=get_the_ID();
	$video_attachment_id=get_post_meta($post_id,'upload-1',true);
	

	
	
	//error_log("The valuessssssss of \$post_id is: " . var_export($post_id, true));
	error_log("The valuessssssss of \$video_attachment_id is: " . var_export($video_attachment_id, true));
	
	// Replace the domain part with the local server path.
	
	

	if ( $video_attachment_id && ! post_password_required() ) :
        $path_info = pathinfo($video_attachment_id);
		$srt_file_path = $path_info['dirname'] . '/' . $path_info['filename'] . '.vtt';
		
		error_log("The valuessssssss of \$srt_file_path is: " . var_export($srt_file_path, true));
        ?>
		<div>
			
			
			<figure id="videoContainer" data-fullscreen="false">
				<video id="video" controls preload="metadata">
                    <source src="<?php echo esc_url( $video_attachment_id ); ?>" type="video/mp4"/>
                    <track kind="subtitles" src="<?php echo esc_url( $srt_file_path ); ?>" srclang="gr" label="Greek" default/>
                    Your browser does not support the video tag.
				</video>
					
			</figure>
	<script>
		var frameData = {
		'motorcycling': ['511', '512', '548', '549', '550', '551', '552', '553', '554', '555', '556', '557', '558', '559', '560', '561'],
		'news anchoring': ['902', '903', '904', '905', '906', '907', '908', '909', '910', '911', '912', '913', '914', '915', '916', '917', '918', '919', '920', '921', '922', '923', '924', '925', '926']
		};

		// Function to create buttons dynamically
		function createButtons(videoType) {
		var buttonsDiv = document.getElementById('buttons');
		buttonsDiv.innerHTML = ''; // Clear previous buttons

		// Get frame numbers for the selected video type
		var frames = frameData[videoType];
		
		// Create buttons for each frame
		frames.forEach(function(frame) {
			var button = document.createElement('button');
			button.textContent = videoType + ' - Frame ' + frame;
			button.onclick = function() {
			seekToFrame(frame);
			};
			buttonsDiv.appendChild(button);
		});
		}

		// Function to seek to a specific frame
		function seekToFrame(frameNumber) {
		var video = document.getElementById("myVideo");
		// Calculate the time to seek based on the frame number
		var timeInSeconds = parseInt(frameNumber) / video.frameRate;
		video.currentTime = timeInSeconds;
		}

		// Call the createButtons function initially for the first video type
		createButtons('motorcycling');

		// Function to change the buttons when a different video type is selected
		function changeVideoType(videoType) {
		createButtons(videoType);
		}

  var audio = document.getElementById('audioPlayer');
  var canvas = document.getElementById('spectrumCanvas');
  var ctx = canvas.getContext('2d');
  var audioContext = new (window.AudioContext || window.webkitAudioContext)();
  var analyser = audioContext.createAnalyser();
  var source = audioContext.createMediaElementSource(audio);

  // Check if the audio source is a WAV file
  var isWAV = audio.canPlayType && audio.canPlayType('audio/wav') !== '';

  if (isWAV) {
    // Connect the source to the analyser
    source.connect(analyser);
    analyser.connect(audioContext.destination);

    // Set up the analyser
    analyser.fftSize = 256;
    var bufferLength = analyser.frequencyBinCount;
    var dataArray = new Uint8Array(bufferLength);

    // Draw the spectrum
    function drawSpectrum() {
      analyser.getByteFrequencyData(dataArray);

      // Clear previous drawings
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      var barWidth = (canvas.width / bufferLength) * 2.5;
      var barHeight;
      var x = 0;

      for (var i = 0; i < bufferLength; i++) {
        barHeight = dataArray[i];

        ctx.fillStyle = 'rgb(' + (barHeight + 100) + ', 50, 50)';
        ctx.fillRect(x, canvas.height - barHeight / 2, barWidth, barHeight / 2);

        x += barWidth + 1;
      }

      requestAnimationFrame(drawSpectrum);
    }

    // Start drawing the spectrum when audio is loaded
    audio.addEventListener('loadedmetadata', function() {
      // Start the audio context when user interacts with the page (e.g., clicks Play)
      document.addEventListener('click', function() {
        audioContext.resume().then(() => {
          console.log('Audio context resumed');
        });
      });

      drawSpectrum();
    });
  }
</script>		
	</div>
		
		

	
    <?php endif; 
	// End of video display
	?>

	
	<?php
	// Get posts format.
	$format = get_post_format();
	
    
    
    
	// Get elements.
	$elements = oceanwp_blog_single_elements_positioning();
	//error_log("The valuessssssss of \$elements is: " . var_export($elements, true));
	// Loop through elements.
	foreach ( $elements as $element ) {

		

		// Title.
		if ( 'title' === $element ) {

			get_template_part( 'partials/single/header' );

		}

		// Meta.
		if ( 'meta' === $element ) {

			get_template_part( 'partials/single/meta' );

		}

		// Content.
		if ( 'content' === $element ) {

			get_template_part( 'partials/single/content' );

		}

		// Tags.
		if ( 'tags' === $element ) {

			get_template_part( 'partials/single/tags' );

			// Check if the user is logged in
			if (is_user_logged_in()) {
				// Get the current user ID
				$current_user_id = get_current_user_id();

				// Get the post author ID
				$post_author_id = get_post_field('post_author', get_the_ID());

				// Check if the current user is the author of the post
				if ($current_user_id == $post_author_id) {
				
					//Edit post shortcode
					echo do_shortcode('[frontend_admin form=2225]');
				}
			}
			

			

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

</article>



