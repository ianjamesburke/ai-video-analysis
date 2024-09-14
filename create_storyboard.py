import cv2
import numpy as np
import math
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use a non-GUI backend
import os
from dotenv import load_dotenv

load_dotenv()



def create_storyboard(original_video_path, num_frames, output_path):

    video_path = reduce_video_size(original_video_path, compression_percentage=.1)

    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    cap.release()
    cap = cv2.VideoCapture(video_path)
    frames = []
    for i in range(num_frames):
        frame_num = math.floor(i * length / num_frames)
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = cap.read()
        if ret:
            frames.append(frame)
    cap.release()
    rows = math.ceil(math.sqrt(num_frames))
    cols = math.ceil(num_frames / rows)
    storyboard = np.zeros((rows * frame_height, cols * frame_width, 3), dtype=np.uint8)
    for i in range(rows):
        for j in range(cols):
            frame_num = i * cols + j
            if frame_num < num_frames:
                frame = frames[frame_num]
                storyboard[i * frame_height:(i + 1) * frame_height, j * frame_width:(j + 1) * frame_width] = frame
    cv2.imwrite(output_path, storyboard)
    plt.imshow(cv2.cvtColor(storyboard, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    # plt.show()
    return output_path
import os

def reduce_video_size(video_path, compression_percentage):
    reduced_video_path = video_path + '_reduced.mp4'
    
    # Check if the reduced video already exists
    if os.path.exists(reduced_video_path):
        print("The video has already been reduced.")
        return reduced_video_path
    
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return None
    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    
    new_width = int(frame_width * compression_percentage)
    new_height = int(frame_height * compression_percentage)
    
    # outputs the video to the same directory as the input video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(reduced_video_path, fourcc, frame_rate, (new_width, new_height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
        out.write(resized_frame)
    
    cap.release()
    out.release()

    return reduced_video_path

def get_video_length_sec(video_path):
    cap = cv2.VideoCapture(video_path)
    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    return math.floor(length / frame_rate)

def get_video_dimensions(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    return frame_width, frame_height

def get_video_fps(video_path):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    return frame_rate



def is_composite(n):
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return True
    return False



def calculate_tile_num(video_path, fps):
    length = get_video_length_sec(video_path)
    biased_value = math.floor(length * fps)
    
    # Find the nearest composite number greater than or equal to the biased value
    while not is_composite(biased_value):
        biased_value += 1

    return biased_value



def main(video_path, output_path):
    # fps = the number of frames per second, smaller number, fewer frames rendered
    tile_num = calculate_tile_num(video_path, fps=1)

    create_storyboard(video_path, tile_num, output_path)

    return tile_num



if __name__ == "__main__":
    try:
        print("TESTING CREATE STORYBOARD")
        main('sample.mp4', 'sample_storyboard.png')
        print("PASSED")
    except Exception as e:
        print(e)
