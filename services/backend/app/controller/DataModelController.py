from app import response, app
from flask import url_for
from werkzeug.utils import secure_filename
import uuid, os, datetime, dlib, cv2
from app.request.DataModel.DataTestStoreRequest import DataTestStoreRequest
from app.helper.preprocessing import get_frames_by_input_video, extract_component_by_images, draw_quiver_and_save_plotlib_image, convert_video_to_webm
from app.helper.helper import convert_video_to_avi, natural_sort_key, get_calculate_from_predict, convert_ndarray_to_list
from app.helper.poc import POC
from app.helper.vektor import Vektor
from app.helper.quadran import Quadran
from app.helper.constant import COMPONENTS_SETUP, FRAMES_DATA_QUADRAN_COMPONENTS, MODEL_PREDICTOR, MODEL_SVM_4QMV, MODEL_SVM_EXTRACTION_FEATURE , QUADRAN_DIMENSIONS, BLOCKSIZE
import joblib
import pandas as pd
import numpy as np

def store():
    request_data = DataTestStoreRequest()
    
    if not request_data.validate():
        return response.error(422, 'Invalid request form validation', request_data.errors)
    
    try:
        # Mendapatkan file dari request
        file = request_data.file.data
        with_preview = request_data.with_preview.data
        filename = secure_filename(file.filename)
        
        # Mendapatkan ekstensi dari filename dengan split
        file_extension = filename.split('.')[-1].lower()
        
        # Misalnya, nama file baru tanpa ekstensi
        new_filename = f'video-{str(uuid.uuid4())}'
        
        # Menggabungkan new_filename dengan ekstensi dan buat path untuk output 
        new_filename_with_extension = f"{new_filename}.{file_extension}"
        file_path_video = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], new_filename_with_extension)
        file_path_output_images = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_IMAGE'], 'output', new_filename)

        # Save video ke folder di lokal
        file.save(file_path_video)

        # # Lakukan pengecekan berdasarkan file extension
        # if file_extension == 'avi':
        #     # Convert AVI ke WEBM untuk respons
        #     converted_webm_filename = f"{new_filename}.webm"
        #     converted_webm_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_webm_filename)
        #     file_path_video_response = convert_video_to_webm(file_path_video, converted_webm_file_path)
        # elif file_extension == 'webm':
        #     # Convert WEBM ke AVI untuk pemrosesan
        #     converted_avi_filename = f"{new_filename}.avi"
        #     converted_avi_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_avi_filename)
        #     convert_video_to_avi(file_path_video, converted_avi_file_path)
        #     file_path_video = converted_avi_file_path
        #     new_filename_with_extension = f"{new_filename}.avi"
        #     file_path_video_response = file_path_video
        # else:
        #     # Convert input video ke AVI untuk pemrosesan
        #     converted_avi_filename = f"{new_filename}.avi"
        #     converted_avi_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_avi_filename)
        #     convert_video_to_avi(file_path_video, converted_avi_file_path)
        #     file_path_video = converted_avi_file_path
        #     new_filename_with_extension = f"{new_filename}.avi"
            
        #     # Convert input video ke WEBM untuk respons
        #     converted_webm_filename = f"{new_filename}.webm"
        #     converted_webm_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_webm_filename)
        #     file_path_video_response = convert_video_to_webm(file_path_video, converted_webm_file_path)
            
        #     # Hapus file input yang bukan AVI atau WEBM setelah konversi
        #     os.remove(file_path_video)
        # return response.success(f"With Preview : {with_preview}")

        if file_extension != 'avi':
            # Convert input video ke AVI untuk pemrosesan
            converted_avi_filename = f"{new_filename}.avi"
            converted_avi_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_avi_filename)
            convert_video_to_avi(file_path_video, converted_avi_file_path)

            # Hapus file input yang bukan AVI atau WEBM setelah konversi
            os.remove(file_path_video)
            # Set file path video yang baru
            file_path_video = converted_avi_file_path
            new_filename_with_extension = converted_avi_filename

        with app.app_context():
            file_path_video_response = url_for('static', filename=file_path_video.replace('\\', '/').replace('assets/', '', 1), _external=True)

        images, error = get_frames_by_input_video(file_path_video, file_path_output_images, 200)
        if error is not None:
            return response.error(message=error)
        
        # Variabel untuk format response sucess output
        output_data = []

        # --- Setup untuk perhitungan POC dari output images ---
        # load model dan shape predictor untuk deteksi wajah
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_MODEL'], MODEL_PREDICTOR))
        
        # Inisialisasi variabel untuk menyimpan data dari masing-masing komponen
        components_setup = COMPONENTS_SETUP
        quadran_dimensions = QUADRAN_DIMENSIONS
        frames_data_quadran_column = FRAMES_DATA_QUADRAN_COMPONENTS
        frames_data_quadran = []
        frames_data_all_component = []
        total_blocks_components = {component_name: 0 for component_name in components_setup}
        data_blocks_first_image = {component_name: None for component_name in components_setup}
        index = {component_name: 0 for component_name in components_setup}

        # Hitung total blok dari masing-masing komponen lalu disetup kedalam total_blocks_components
        for component_name, component_info in components_setup.items():
            total_blocks_components[component_name] = int((component_info['object_dimension']['width'] / BLOCKSIZE) * (component_info['object_dimension']['height'] / BLOCKSIZE))

        # looping semua file yang ada didalam
        for filename in sorted(os.listdir(file_path_output_images), key=natural_sort_key):
            if filename.endswith(".jpg") or filename.endswith(".png"): 
                image = cv2.imread(os.path.join(file_path_output_images, filename))
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                
                # Deteksi shape muka didalam grayscale image
                rects = detector(gray)
                
                if with_preview:
                    # Set variabel current_image_data untuk response data dari masing-masing frame
                    current_image_data = {
                        "name": filename,
                        "url": next((img['url'] for img in images if os.path.splitext(img['name'])[0] == os.path.splitext(filename)[0]), None),
                        "components": {}
                    }

                if not index[component_name] == 0:
                    # Buat variabel frames_data_all_component untuk menampung data current frame
                    frame_data_all_component = {'Frame': f"{index[component_name] + 1}({filename.split('.')[0]})"}
                    # Buat variabel frame_data_quadran untuk menampung data current frame
                    frame_data_quadran = {'Frame': f"{index[component_name] + 1}({filename.split('.')[0]})"}

                # Memproses rects untuk setiap bentuk wajah yang terdeteksi
                for rect in rects:
                    # Ambil bentuk wajah dalam bentuk shape sesuai dengan model predictor
                    shape = predictor(gray, rect)
                    # Memproses setiap komponen wajah
                    for component_name, component_info in components_setup.items():
                        # print(f"\n{"test"}-{filename.split('.')[0]}-{component_info['object_name']}:")
                        # Inisialisasi variabel sum_data_by_quadran untuk menyimpan data hasil quadran
                        sum_data_by_quadran = {}

                        # Looping untuk setiap atribut dalam frames_data_quadran_column
                        for column in frames_data_quadran_column:
                            # Inisialisasi sub-dictionary untuk setiap atribut dalam frames_data_quadran_column yang defaultnya 0
                            sum_data_by_quadran[column] = {quadrant: 0 for quadrant in quadran_dimensions}
                        
                        # Ambil data blok image dari return fungsi extract_component_by_images
                        data_blocks_image_current, image_url = extract_component_by_images(
                            image=image,
                            shape=shape,
                            frameName=filename.split(".")[0], 
                            objectName=component_info['object_name'],
                            objectRectangle=component_info['object_rectangle'],
                            pixelShifting=component_info['pixel_shifting'],
                            objectDimension=component_info['object_dimension'],
                            directoryOutputImage=file_path_output_images,
                            withPreview=with_preview
                        )

                        if with_preview:
                            # Tambahkan url image kedalam current_image_data
                            current_image_data["components"][component_name] = {
                                "url_source": image_url
                            }
                        
                        # Ambil frame pertama dari perulangan lalu simpan di variabel dan skip (lanjutkan ke frame berikut)
                        if data_blocks_first_image[component_name] is None:
                            # Set value data_blocks_first_image[component_name] ke data_blocks_image_current
                            data_blocks_first_image[component_name] = data_blocks_image_current
                            # Skip looping nya ke looping selanjutnya
                            continue

                        # # Tampilkan data block image current ke matplotlib
                        # plt.imshow(np.uint8(data_blocks_image_current), cmap="gray")

                        # Inisiasi class POC
                        initPOC = POC(data_blocks_first_image[component_name], data_blocks_image_current, BLOCKSIZE) 
                        # Pemanggilan fungsi pocCalc() untuk menghitung nilai POC disetiap gambar
                        valPOC = initPOC.getPOC() 

                        # Pemanggilan class dan method untuk menampilkan quiver / gambar panah
                        initQuiv = Vektor(valPOC, BLOCKSIZE)
                        quivData = initQuiv.getVektor() 

                        # Pemanggilan class untuk mengeluarkan nilai karakteristik vektor dan quadran
                        initQuadran = Quadran(quivData) 
                        quadran = initQuadran.getQuadran()

                        if with_preview:
                            # Tampilkan gambar grayscale dengan quiver dan simpan plot nya
                            # plt.quiver(quivData[:, 0], quivData[:, 1], quivData[:, 2], quivData[:, 3], scale=1, scale_units='xy', angles='xy', color="r")    
                            url_result = draw_quiver_and_save_plotlib_image(
                                dataBlockImage=data_blocks_image_current, 
                                quivData=quivData,
                                frameName=filename.split(".")[0],
                                objectName=component_info['object_name'], 
                                directoryOutputImage=file_path_output_images
                            )
                            
                            if with_preview:
                                current_image_data["components"][component_name]["url_result"] = url_result

                        # print(tabulate(quadran, headers=['Blok Ke', 'X', 'Y', 'Tetha', 'Magnitude', 'Quadran Ke']))

                        # Update frame_data dengan data quadran
                        for i, quad in enumerate(quadran):
                            # --- Setup bagian Nilai fitur (semua) Dataset ---
                            # Set data kedalam frame_data_all_component sesuai columnnya
                            frame_data_all_component[f'{component_name}-X{i+1}'] = quad[1]
                            frame_data_all_component[f'{component_name}-Y{i+1}'] = quad[2]
                            frame_data_all_component[f'{component_name}-Tetha{i+1}'] = quad[3]
                            frame_data_all_component[f'{component_name}-Magnitude{i+1}'] = quad[4]

                            # --- Setup bagian 4qmv Dataset ---
                            # Cek apakah quad[5] ada didalam array quadran_dimensions
                            if quad[5] in quadran_dimensions:
                                # Tambahkan nilai quad[1] ke sumX pada kuadran yang sesuai
                                sum_data_by_quadran['sumX'][quad[5]] += quad[1]
                                # Tambahkan nilai quad[2] ke sumY pada kuadran yang sesuai
                                sum_data_by_quadran['sumY'][quad[5]] += quad[2]
                                # Tambahkan nilai quad[3] ke Tetha pada kuadran yang sesuai
                                sum_data_by_quadran['Tetha'][quad[5]] += quad[3]
                                # Tambahkan nilai quad[4] ke Magnitude pada kuadran yang sesuai
                                sum_data_by_quadran['Magnitude'][quad[5]] += quad[4]
                                # Tambahkan jumlah quadran sesuai dengan quad[5] ke JumlahQuadran pada kuadran yang sesuai
                                sum_data_by_quadran['JumlahQuadran'][quad[5]] += 1

                        # --- Setup bagian 4qmv Dataset ---
                        # Inisialisasi data untuk setiap blok dan setiap kuadran dengan nilai sesuai sum_data_by_quadran
                        for quadran in quadran_dimensions:
                            for feature in frames_data_quadran_column:
                                # Buat nama kolom dengan menggunakan template yang diberikan
                                column_name = f"{component_name}_{feature}_{quadran}"
                                # Set value sum_data_by_quadran[feature][quadran] ke frame_data_quadran sesuai column_name nya
                                frame_data_quadran[column_name] = sum_data_by_quadran[feature][quadran]

                if not index[component_name] == 0:
                    # --- Setup bagian 4qmv Dataset ---
                    # Append data frame ke list frames_data_quadran untuk 4qmv
                    frames_data_quadran.append(frame_data_quadran)
                    # Tambahkan kolom "Folder Path" dengan nilai folder saat ini
                    frame_data_quadran['Folder Path'] = "data_test"
                    # Tambahkan kolom "Label" dengan nilai label saat ini
                    frame_data_quadran['Label'] = "data_test"

                    # --- Setup bagian Nilai fitur (semua) Dataset ---
                    # Append data frame ke list frames_data_quadran untuk 4qmv
                    frames_data_all_component.append(frame_data_all_component)
                    # Tambahkan kolom "Folder Path" dengan nilai folder saat ini
                    frame_data_all_component['Folder Path'] = "data_test"
                    # Tambahkan kolom "Label" dengan nilai label saat ini
                    frame_data_all_component['Label'] = "data_test"

                # Update index per component_name
                index[component_name] += 1  

                if with_preview:
                    # Append current_image_data ke output_data
                    output_data.append(current_image_data)

        # Membuat direktori jika belum ada untuk outputnya
        output_csv_dir = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_DATA'], new_filename))
        os.makedirs(output_csv_dir, exist_ok=True)

        # --- Setup bagian Nilai fitur (semua) Dataset ---
        # Initialisasi dataframe dengan pandas
        df_fitur_all = pd.DataFrame(frames_data_all_component)
        # Simpan ke file CSV
        df_fitur_all.to_csv(os.path.join(output_csv_dir, 'nilai-fitur-all-component.csv'), index=False, float_format=None)

        # --- Setup bagian 4qmv Dataset ---
        # Initialisasi dataframe dengan pandas
        df_quadran = pd.DataFrame(frames_data_quadran)
        # Simpan ke file CSV
        df_quadran.to_csv(os.path.join(output_csv_dir, '4qmv-all-component.csv'), index=False, float_format=None)
        
        # Base path model joblib
        base_model_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_MODEL'])
        # Kolom yang akan dihapus
        except_feature_columns = ['Frame', 'Folder Path', 'Label']

        # Variabel set model dengan random_sampling dan kfold
        model_variabel_set = {
            "random_sampling": {
                "fitur_all_component": {
                    "data": df_fitur_all,
                    "model_path": os.path.join(base_model_path, 'svm_model_random_sampling.joblib'),
                    "except_feature_columns": except_feature_columns,
                    "label_encoder_path": os.path.join(base_model_path, 'label_encoder_random_sampling.joblib')
                },
                "4qmv_all_component": {
                    "data": df_quadran,
                    "model_path": os.path.join(base_model_path, '4qmv_svm_model_random_sampling.joblib'),
                    "except_feature_columns": except_feature_columns,
                    "label_encoder_path": os.path.join(base_model_path, '4qmv_label_encoder_random_sampling.joblib')
                }
            },
            "kfold": {
                "fitur_all_component": {
                    "data": df_fitur_all,
                    "model_path": os.path.join(base_model_path, 'svm_model_kfold.joblib'),
                    "except_feature_columns": except_feature_columns,
                    "label_encoder_path": os.path.join(base_model_path, 'label_encoder_kfold.joblib')
                },
                "4qmv_all_component": {
                    "data": df_quadran,
                    "model_path": os.path.join(base_model_path, '4qmv_svm_model_kfold.joblib'),
                    "except_feature_columns": except_feature_columns,
                    "label_encoder_path": os.path.join(base_model_path, '4qmv_label_encoder_kfold.joblib')
                }
            }
        }

        # Setup response data prediction untuk di return json
        response_data = {
            "video": {
                "url": file_path_video_response, 
                "name": new_filename_with_extension,
            },
            # "result": result_prediction,
            # "list_predictions" : list_predictions,
            # "array_predictions": decoded_predictions.tolist()
        }
        
        # Melakukan prediksi untuk setiap variabel set dan komponen
        predictions_result_all = {}
        for train_model_key, train_model_data in model_variabel_set.items():
            predictions_result_all[train_model_key] = {}
            for metode_key, metode_data in train_model_data.items():
                df = metode_data['data']
                model_path = metode_data['model_path']
                except_columns = metode_data['except_feature_columns']
                label_encoder_path = metode_data['label_encoder_path']
                
                # Hapus kolom yang tidak diperlukan
                df = df.drop(columns=except_columns)
                
                # Load model dan label encoder
                svm_model = joblib.load(model_path)
                label_encoder = joblib.load(label_encoder_path)
                
                # Lakukan prediksi dan decoded prediksi
                predictions = svm_model.predict(df.values)
                decoded_predictions = label_encoder.inverse_transform(predictions)
                
                # Dapatkan hasil kalkulasi dari prediksi
                result_prediction, list_predictions = get_calculate_from_predict(decoded_predictions)
                
                # Simpan hasil dalam predictions_result_all
                predictions_result_all[train_model_key][metode_key] = {
                    "decoded_predictions": decoded_predictions,
                    "result_prediction": result_prediction,
                    "list_predictions": list_predictions,
                }

        if with_preview:
            # Mengisi output_data dengan prediksi yang sesuai
            for i in range(len(output_data)):
                if i == 0:
                    output_data[i]['prediction'] = None
                else:
                    prediction_entry = {}
                    for train_model_key in model_variabel_set.keys():
                        for metode_key in model_variabel_set[train_model_key].keys():
                            prediction_entry[f"{metode_key}_with_{train_model_key}"] = predictions_result_all[train_model_key][metode_key]['decoded_predictions'][i-1]
                    output_data[i]['prediction'] = prediction_entry

        # Menyiapkan response_data dengan array_predictions, result, dan list_predictions
        array_predictions = {}
        result_predictions = {}
        list_predictions_all = {}
        for train_model_key, components in model_variabel_set.items():
            for metode_key in components.keys():
                key_name = f"{metode_key}_with_{train_model_key}"
                # Konversi ndarray menjadi list
                array_predictions[key_name] = predictions_result_all[train_model_key][metode_key]['decoded_predictions'].tolist()
                result_predictions[key_name] = predictions_result_all[train_model_key][metode_key]['result_prediction']
                list_predictions_all[key_name] = predictions_result_all[train_model_key][metode_key]['list_predictions']

        response_data = {
            "array_predictions": array_predictions,
            "result": result_predictions,
            "list_predictions": list_predictions_all
        }

        if with_preview:
            response_data["images"] = [item.tolist() if isinstance(item, np.ndarray) else item for item in output_data]
        
        # print(type(array_predictions))
        # print(type(result_predictions))
        # print(type(list_predictions_all))
        # print(type(output_data))
        return response.success(200, 'Ok', response_data)
    except Exception as e:
        return response.error(message=str(e))
