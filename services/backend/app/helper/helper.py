import numpy as np
import cv2, re
from collections import Counter

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

def get_calculate_from_predict(list_decoded_predictions):
    # Hitung jumlah kemunculan setiap kategori dalam array hasil prediksi
    prediction_counts = Counter(list_decoded_predictions)

    # Hitung total jumlah prediksi
    total_predictions = len(list_decoded_predictions)

    # Inisialisasi variabel untuk menyimpan kategori terbanyak dan jumlahnya
    most_common_category = None
    most_common_count = 0
    
    # Inisialisasi variabel untuk menyimpan hasil prediksi
    result_prediction = None

    # Buat dictionary untuk menyimpan hasil analisis prediksi
    list_predictions = {}

    # Lakukan iterasi melalui hasil prediksi
    for category, count in prediction_counts.items():
        # Hitung persentase dari setiap kategori
        percentage = (count / total_predictions) * 100

        # Tambahkan informasi jumlah dan persentase ke dictionary
        list_predictions[category] = {
            "count": count,
            "percentage": format_number_and_round(percentage)
        }

        # Periksa apakah kategori saat ini memiliki jumlah terbanyak
        if count > most_common_count:
            most_common_count = count
            most_common_category = category

    # Set hasil prediksi sebagai kategori terbanyak
    result_prediction = most_common_category
    return result_prediction, list_predictions

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]
