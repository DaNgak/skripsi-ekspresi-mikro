import cv2, os
from flask import url_for
from app import app

import numpy as np
from typing import Literal, TypedDict

class ObjectRectangle(TypedDict):
    x_right: int
    x_left: int
    y_highest: int
    y_lowest: int

class PixelShifting(TypedDict):
    pixel_x: int
    pixel_y: int

class ObjectDimension(TypedDict):
    width: int
    height: int

def extract_component_by_images(
    image,
    shape,
    frameName,
    objectName: Literal[
        "mouth",
        "eye_left",
        "eye_right",
        "eyebrow_left",
        "eyebrow_right",
    ],
    objectRectangle: ObjectRectangle,
    pixelShifting: PixelShifting,
    objectDimension: ObjectDimension,
    directoryOutputImage,
):
    # Setup shape part dari parameter objectRectangle
    x_right = shape.part(objectRectangle["x_right"]).x
    x_left = shape.part(objectRectangle["x_left"]).x
    y_highest = shape.part(objectRectangle["y_highest"]).y
    y_lowest = shape.part(objectRectangle["y_lowest"]).y

    # print(f'objectName = {objectName}' )
    # print(f'objectRectangle = {objectRectangle}' )
    # print(f'pixelShifting = {pixelShifting}' )
    # print(f'objectDimension = {objectDimension}' )
    # print(f'x_left = {x_left}' )
    # print(f'x_right = {x_right}' )

    width_object = x_right - x_left
    height_object = y_lowest - y_highest

    # Menggeser tepi kiri sisi gambar sebanyak variabel pergeseran_pixel ke kiri
    x_left -= pixelShifting["pixel_x"]
    # Menggeser tepi atas sisi gambar sebanyak variabel pergeseran_pixel ke atas
    y_highest -= pixelShifting["pixel_y"]

    # Memastikan koordinat tetap berada dalam batas size gambar
    x_left = max(0, x_left)
    y_highest = max(0, y_highest)
    width_object = min(objectDimension["width"], image.shape[1] - x_left)
    height_object = min(objectDimension["height"], image.shape[0] - y_highest)

    # Create directory if it doesn't exist
    os.makedirs(os.path.join(directoryOutputImage, objectName), exist_ok=True)

    selected_component_image = image.copy()

    selected_component_image = image.copy()[y_highest:y_highest + height_object + 1, x_left:x_left + width_object + 1]

    # Grayscale the image
    selected_component_image_gray = cv2.cvtColor(
        selected_component_image, cv2.COLOR_BGR2GRAY
    )
    
    filepath = os.path.join(directoryOutputImage, objectName, f"{frameName:02}.jpg")

    if cv2.imwrite(filepath, selected_component_image_gray):
        with app.app_context():
            # Dapatkan URL dari gambar yang disimpan
            image_url = url_for('static', filename=filepath.replace('\\', '/').replace('assets/', '', 1), _external=True)

    return np.array(selected_component_image_gray), image_url

def get_frames_by_input_video(pathInputVideo, pathOutputImage, framePerSecond=60):
    images = []  # Array untuk menyimpan informasi gambar
    error = None  # Variabel untuk menyimpan pesan kesalahan
    
    # Cek apakah file video terdeteksi
    if not os.path.exists(pathInputVideo):
        error = f"Path to file {pathInputVideo} is not valid"
        return images, error

    # Convert path video ke video capture
    vidcap = cv2.VideoCapture(f'{pathInputVideo}')
    if not vidcap.isOpened():
        error = f"Failed to open video {pathInputVideo}"
        return images, error

    # Buat path directory untuk output gambar jika tidak ada
    if not os.path.exists(pathOutputImage):
        os.makedirs(pathOutputImage)

    count = 1

    while True:
        # Read setiap frame dari video (setiap looping framenya bertambah 1 sampai jumlah frame video habis baru success bernilai false)
        success, image = vidcap.read()
        if not success:
            break

        # Buat nama file gambar
        filename = f"img{count}.jpg"
        filepath = os.path.join(pathOutputImage, filename)

        # Simpan gambar sebagai jpg
        if cv2.imwrite(filepath, image):
            with app.app_context():
                # Dapatkan URL dari gambar yang disimpan

                image_url = url_for('static', filename=filepath.replace('\\', '/').replace('assets/', '', 1), _external=True)
                images.append({
                    'name': f"img{count}",
                    'url': image_url
                })

        # count ++ untuk melanjutkan looping ke frame berikutnya
        count += 1
        
        # Hitung waktu diambilnya frame ke sekian detik dari durasi video 
        expected_frame_time = count / framePerSecond
        
        # Set waktu frame yang diambil 
        vidcap.set(cv2.CAP_PROP_POS_MSEC, expected_frame_time * 1000)

    # Jangan lupa untuk merilis capture object
    vidcap.release()
    
    return images, error