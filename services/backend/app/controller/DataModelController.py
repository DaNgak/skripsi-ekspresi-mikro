from app import response, app
from werkzeug.utils import secure_filename
import uuid, os, datetime
import cv2
from app.request.DataModel.DataTestStoreRequest import DataTestStoreRequest
from app.helper.preprocessing import get_frames_by_input_video
from app.helper.helper import convert_video_to_avi

def store():
    request_data = DataTestStoreRequest()
    
    if not request_data.validate():
        return response.error(422, 'Invalid request form validation', request_data.errors)
    
    try:
        # Mendapatkan file dari request
        file = request_data.file.data
        filename = secure_filename(file.filename)
        
        # Mendapatkan ekstensi dari filename dengan split
        file_extension = filename.split('.')[-1]
        
        # Misalnya, nama file baru tanpa ekstensi
        new_filename = f'video-{str(uuid.uuid4())}'
        
        # Menggabungkan new_filename dengan ekstensi dan buat path untuk output 
        new_filename_with_extension = f"{new_filename}.{file_extension}"
        file_path_video = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], new_filename_with_extension)
        file_path_output_images = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_IMAGE'], 'output', new_filename)

        # Save video ke folder di lokal
        file.save(file_path_video)

        # Check jika format bukan AVI maka convert ke AVI
        if file_extension != 'avi':
            converted_avi_filename = f"{new_filename}.avi"
            converted_avi_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_avi_filename)
            convert_video_to_avi(file_path_video, converted_avi_file_path)
            # Hapus file yang sebelumnya bukan format AVI
            os.remove(file_path_video)
            file_path_video = converted_avi_file_path

        images, error = get_frames_by_input_video(file_path_video, file_path_output_images)
        if error is not None:
            return response.error(message=error)

        # for filename in os.listdir(file_path):
        #     if filename.endswith(".jpg") or filename.endswith(".png"): 
        #         # Create the directory if it doesn't exist
        #         image = cv2.imread(os.path.join(file_path, filename))
        #         image = cv2.resize(image, (600, 500))
        #         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        #         # detect the faces
        #         rects = detector(gray)

        # Construct the URL path to the uploaded video file
        # url_path = url_for('static', filename=new_filename)
        return response.success(200, 'Ok', {
            "url_path": images,
        })
    except Exception as e:
        return response.error(message=str(e))

