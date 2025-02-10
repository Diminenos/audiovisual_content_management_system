import json
import random
from collections import deque
from operator import itemgetter
import gc
import cv2
import mmengine
import numpy as np
import torch
from mmengine import Config, DictAction
from mmengine.dataset import Compose
import sys
sys.path.insert(0, '/opt/EfficientAT-main/')
from mmaction.apis import inference_recognizer, init_recognizer

from concurrent.futures import ThreadPoolExecutor
from video_updates import update_action_tag
import logging
import logger_config
from help_func_action_button import get_fps, filter_predictions, convert_json_format
from predict_static_video import is_static_video
import os 

# Set up logging
logger_config.setup_logging()
logger = logging.getLogger(__name__)

# Constants for OpenCV
FONTFACE = cv2.FONT_HERSHEY_COMPLEX_SMALL
FONTSCALE = 1
THICKNESS = 1
LINETYPE = 1

EXCLUDED_STEPS = [
    'OpenCVInit', 'OpenCVDecode', 'DecordInit', 'DecordDecode', 'PyAVInit',
    'PyAVDecode', 'RawFrameDecode'
]

def load_action_algo():
    """Load action algorithm and model configuration."""
    try:
        # Hardcoded values
        config_path = '/home/dimineno/Desktop/tsn_imagenet-pretrained-r50_8xb32-1x1x8-100e_kinetics400-rgb.py'
        checkpoint_path = '/home/dimineno/Desktop/tsn_imagenet-pretrained-r50_8xb32-1x1x8-100e_kinetics400-rgb_20220906-2692d16c.pth'
        label_file = '/home/dimineno/Desktop/label_map_k400.txt'
        out_file = '/home/dimineno/Desktop/output.json'  

        cfg = Config.fromfile(config_path)
        cfg.merge_from_dict({})

        data = dict(img_shape=None, modality='RGB', label=-1)
        with open(label_file, 'r') as f:
            label = [line.strip() for line in f]

        model = init_recognizer(cfg, checkpoint_path, device='cuda:0')  
        threshold = 0.01
        stride = 0
        input_step = 1
        label_color = (255, 255, 255)
        msg_color = (128, 128, 128)

        # Prepare test pipeline from non-camera pipeline
        cfg = model.cfg
        sample_length = 4
        pipeline = cfg.test_pipeline
        pipeline_ = pipeline.copy()
        for step in pipeline:
            if 'SampleFrames' in step['type']:
                sample_length = step['clip_len'] * step['num_clips']
                data['num_clips'] = step['num_clips']
                data['clip_len'] = step['clip_len']
                pipeline_.remove(step)
            if step['type'] in EXCLUDED_STEPS:
                # Remove step to decode frames
                pipeline_.remove(step)
        pipeline_.insert(1, dict(type='ArrayDecode'))
        test_pipeline = Compose(pipeline_)

        assert sample_length > 0
        return sample_length, input_step, out_file, threshold, stride, model, data, label, test_pipeline

    except Exception as e:
        logger.exception("Error loading action algorithm: %s", e)
        return None, None, None, None, None, None, None, None, None  # Return None values on failure


def action_algorithm(post_id, video_path, sample_length, input_step, out_file, threshold, stride, model, data, label, test_pipeline):
    """Run the action recognition algorithm."""
    result = 'default.json'
    try:
        
        def get_results_json(result_queue, text_info, thr, msg, ind, out_json):
            if len(result_queue) != 0:
                text_info = {}
                results = result_queue.popleft()
                for i, result in enumerate(results):
                    selected_label, score = result
                    if score < thr:
                        break
                    text_info[i + 1] = selected_label + ': ' + str(round(score, 2))
                out_json[ind] = text_info
            elif len(text_info):
                out_json[ind] = text_info
            else:
                out_json[ind] = msg
            return text_info, out_json

        def show_results(model, data, label):
            """Display the results of the model on the input video."""
            try:
                frame_queue = deque(maxlen=sample_length)
                result_queue = deque(maxlen=1)

                cap = cv2.VideoCapture(video_path)
                num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

                msg = 'Preparing action recognition ...'
                text_info = {}
                out_json = {}

                ind = 0
                prog_bar = mmengine.ProgressBar(num_frames)
                backup_frames = []

                while ind < num_frames:
                    ind += 1
                    prog_bar.update()
                    ret, frame = cap.read()
                    if frame is None:
                        # Drop it when encountering None
                        continue
                    backup_frames.append(np.array(frame)[:, :, ::-1])
                    if ind == sample_length:
                        # Provide a quick show at the beginning
                        frame_queue.extend(backup_frames)
                        backup_frames = []
                    elif ((len(backup_frames) == input_step
                          and ind > sample_length) or ind == num_frames):
                        # Pick a frame from the backup
                        chosen_frame = random.choice(backup_frames)
                        backup_frames = []
                        frame_queue.append(chosen_frame)

                    ret, scores = inference(model, data, frame_queue)

                    if ret:
                        num_selected_labels = min(len(label), 5)
                        scores_tuples = tuple(zip(label, scores))
                        scores_sorted = sorted(
                            scores_tuples, key=itemgetter(1), reverse=True)
                        results = scores_sorted[:num_selected_labels]
                        result_queue.append(results)

                    if out_file.endswith('.json'):
                        text_info, out_json = get_results_json(result_queue, text_info,
                                                                threshold, msg, ind,
                                                                out_json)

                cap.release()
                cv2.destroyAllWindows()
                if out_file.endswith('.json'):
                    with open(out_file, 'w') as js:
                        json.dump(out_json, js)

            except Exception as e:
                logger.error("Error in show_results: %s", e)

        def inference(model, data, frame_queue):
            """Run inference on the input frames."""
            try:
                if len(frame_queue) != sample_length:
                    # Do not perform inference when there are not enough frames
                    return False, None

                cur_windows = list(np.array(frame_queue))
                if data['img_shape'] is None:
                    data['img_shape'] = frame_queue[0].shape[:2]

                cur_data = data.copy()
                cur_data.update(
                    dict(
                        array=cur_windows,
                        modality='RGB',
                        frame_inds=np.arange(sample_length)))

                result = inference_recognizer(model, cur_data, test_pipeline=test_pipeline)
                scores = result.pred_score.tolist()

                if stride > 0:
                    pred_stride = int(sample_length * stride)
                    for _ in range(pred_stride):
                        frame_queue.popleft()

                # For the case ``stride=0`` deque will automatically popleft one element
                return True, scores

            except Exception as e:
                logger.error("Error in inference function: %s", e)
                return False, None

        show_results(model, data, label)
        result = out_file

        # Open the JSON file in read mode
        with open(result, "r") as json_file:
           
            result = json.load(json_file)

        # Initialize an empty set to store unique class names
        unique_class_names = set()

        # Loop through each element in the JSON data
        for key, value in result.items():
            # Check if the value is a dictionary (contains class names with scores)
            if isinstance(value, dict):
                # Loop through the class names and scores in the dictionary
                for class_name, score_str in value.items():
                    # Split the string to extract the score
                    score = float(score_str.split(': ')[1])
                    if score > 0.8:
                        unique_class_names.add(score_str.split(': ')[0])

        class_names = list(unique_class_names)
        logger.info(f'Task completed with result: {class_names}')
        
        # Update video tags
        update_action_tag(post_id, class_names)

        # Procedure to create hyperlinks to videos based on the action algo results
        # Get FPS for the video file
        fps = get_fps(video_path)
        # Convert the input JSON
        output_data = convert_json_format(result)
        first_occurrences, output = filter_predictions(output_data)

        # Add FPS to first_occurrences to store in JSON
        if fps:
            first_occurrences['fps'] = fps

        # Save the first occurrences JSON, including FPS
        json_path = os.path.splitext(video_path)[0] + '.json'
        with open(json_path, 'w') as output_json_file:
            json.dump(first_occurrences, output_json_file, indent=4)

        logger.info(f"JSON saved with first occurrences and FPS at: {json_path}")

    except Exception as e:
        logger.exception("Error in action_algorithm: %s", e)
    

if __name__ == '__main__':
    post_id = sys.argv[1]  
    file_path = sys.argv[2]

    # Check if the file extension is .mp4
    if not file_path.lower().endswith('.mp4'):
        logger.info(f"Invalid file format: {file_path}. Only .mp4 files are supported. Skipping action recognition.")
    else:
        # Check if video is static before running action recognition
        if is_static_video(file_path):
            logger.info("Video is static. Skipping action recognition.")
        else:
            sample_length, input_step, out_file, threshold, stride, model, data, label, test_pipeline = load_action_algo()
            if model:  
                action_algorithm(post_id, file_path, sample_length, input_step, out_file, threshold, stride, model, data, label, test_pipeline)
