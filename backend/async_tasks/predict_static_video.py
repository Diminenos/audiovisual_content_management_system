import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim

#Check if a video is static
def is_static_video(video_path, ssim_threshold=0.99, frame_skip=50):

    cap = cv2.VideoCapture(video_path)
    ret, prev_frame = cap.read()
    
    if not ret:
        return True  # Considered static if the video cannot be read

    # Convert the first frame to grayscale
    prev_frame_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

    while True:
        # Skip frames to reduce processing time
        for _ in range(frame_skip):
            cap.grab()
        
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert current frame to grayscale
        current_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Calculate SSIM (structural similarity index) between frames
        similarity, _ = ssim(prev_frame_gray, current_frame_gray, full=True)
        
        # Check if similarity is below the threshold, indicating a non-static frame
        if similarity < ssim_threshold:
            cap.release()
            return False  # Video has some motion

        prev_frame_gray = current_frame_gray
    
    cap.release()
    return True  # Video is static



