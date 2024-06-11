import numpy as np
import cv2, re

def average(arr):
    unique, counts = np.unique(arr, return_counts=True)
    max_count_index = np.argmax(counts)
    return unique[max_count_index]

def format_number_and_round_numpy(number):
    if isinstance(number, np.int32) or isinstance(number, int):
        return np.int_(number)
    elif isinstance(number, float):
        return np.float_(round(number, 3))
    else:
        raise ValueError("Invalid number type")
    
def format_number_and_round(number):
    # Jika number merupakan bilangan bulat, hapus desimal
    if number.is_integer():
        return int(number)
    elif isinstance(number, float):
        return float(round(number, 3))
    else:
        raise ValueError("Invalid number type")
    
def convert_video_to_avi(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = None

    if cap.isOpened():
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)

    cap.release()
    if out is not None:
        out.release()

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]
