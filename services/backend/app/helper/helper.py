from collections import Counter
import numpy as np
import cv2, re

def average(arr):
    unique, counts = np.unique(arr, return_counts=True)
    max_count_index = np.argmax(counts)
    return unique[max_count_index]

def to_snake_case(string):
    # Ubah menjadi lowercase dan ganti spasi dengan underscore
    string = string.lower()
    return re.sub(r'\s+', '_', string)

def format_number_and_round_numpy(number):
    if isinstance(number, np.int32) or isinstance(number, int):
        return np.int_(number)
    elif isinstance(number, float):
        return np.float_(round(number, 3))
    else:
        raise ValueError("Invalid number type")
    
def format_number_and_round(number, decimal_places=3):
    # Jika number merupakan bilangan bulat, hapus desimal
    if number.is_integer():
        return int(number)
    elif isinstance(number, float):
        return float(round(number, decimal_places))
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

    # Inisialisasi variabel untuk menyimpan kategori terbanyak (hasilnya) dan jumlahnya dan array list kategori
    result_prediction = None
    most_common_count = 0
    list_predictions = []

    # Lakukan iterasi melalui hasil prediksi
    for category, count in prediction_counts.items():
        # Hitung persentase dari setiap kategori
        percentage = (count / total_predictions) * 100

        # Tambahkan informasi jumlah dan persentase ke list
        list_predictions.append({
            "name": category,
            "count": count,
            "percentage": format_number_and_round(percentage, 2)
        })

        # Periksa apakah kategori saat ini memiliki jumlah terbanyak
        if count > most_common_count:
            most_common_count = count
            result_prediction = category

    return result_prediction, list_predictions

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split('(\d+)', s)]

def convert_ndarray_to_list(obj):
    if isinstance(obj, np.ndarray):
        print("satu")
        return obj.tolist()
    elif isinstance(obj, list):
        print("dua")
        return [convert_ndarray_to_list(item) for item in obj]
    elif isinstance(obj, dict):
        print("tiga")
        return {key: convert_ndarray_to_list(value) for key, value in obj.items()}
    else:
        print("empat")
        return obj