import cv2, os
from flask import url_for
from app import app

# Buat fungsi agar bisa dipanggil di codebase main (nantinya)
# def get_frames_by_input_video(pathInputVideo, pathOutputImage, framePerSecond=60):
#     images = []  # Array untuk menyimpan informasi gambar
#     error = None  # Variabel untuk menyimpan pesan kesalahan
    
#     # Cek apakah file video terdeteksi
#     if not os.path.exists(pathInputVideo):
#         error = f"Path to file {pathInputVideo} is not valid"
#         return images, error

#     # Convert path video ke video capture
#     vidcap = cv2.VideoCapture(f'{pathInputVideo}')
#     if not vidcap.isOpened():
#         error = f"Failed to open video {pathInputVideo}"
#         return images, error

#     # Buat path directory untuk output gambar jika tidak ada
#     if not os.path.exists(pathOutputImage):
#         os.makedirs(pathOutputImage)

#     count = 1

#     while True:
#         # Read setiap frame dari video (setiap looping framenya bertambah 1 sampai jumlah frame video habis baru success bernilai false)
#         success, image = vidcap.read()
#         if not success:
#             break

#         # Buat nama file gambar
#         filename = f"img{count}.jpg"
#         filepath = os.path.join(pathOutputImage, filename)
#         # print path aplikasi sekarang dijalankan
#         filepath_cv2 = os.path.join(app.config['UPLOAD_FOLDER'] ,filepath)
#         filepath_cv2 = f'test/test-juga/{filename}'

#         # Simpan gambar sebagai jpg
#         if cv2.imwrite(filepath_cv2, image):
#             with app.app_context():
#                 # Dapatkan URL dari gambar yang disimpan
#                 image_url = url_for('static', filename=filepath.replace('\\', '/'), _external=True)
#                 images.append({
#                     'name': f"img{count}",
#                     'url': image_url
#                 })


#         # count ++ untuk melanjutkan looping ke frame berikutnya
#         count += 1
        
#         # Hitung waktu diambilnya frame ke sekian detik dari durasi video 
#         expected_frame_time = count / framePerSecond
        
#         # Set waktu frame yang diambil 
#         vidcap.set(cv2.CAP_PROP_POS_MSEC, expected_frame_time * 1000)

#     # Jangan lupa untuk merilis capture object
#     vidcap.release()
    
#     return images, error

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