from app import response, app
from werkzeug.utils import secure_filename
import uuid, os, datetime, dlib, cv2
from app.request.DataModel.DataTestStoreRequest import DataTestStoreRequest
from app.helper.preprocessing import get_frames_by_input_video, extract_component_by_images
from app.helper.helper import convert_video_to_avi, natural_sort_key, get_calculate_from_predict
from app.helper.poc import POC
from app.helper.vektor import Vektor
from app.helper.quadran import Quadran
from app.helper.constant import COMPONENTS_SETUP, FRAMES_DATA_QUADRAN_COMPONENTS, MODEL_PREDICTOR, MODEL_SVM_4QMV, MODEL_SVM_EXTRACTION_FEATURE , QUADRAN_DIMENSIONS, BLOCKSIZE
import joblib
import pandas as pd


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
            new_filename_with_extension = f"{new_filename}.avi"

        images, error = get_frames_by_input_video(file_path_video, file_path_output_images)
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
        frames_data = {component_name: [] for component_name in components_setup}
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
                        # Buat variabel frame_data untuk menampung data current frame
                        frame_data = {'Frame': f"{index[component_name] + 1}({filename.split('.')[0]})"}

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
                            directoryOutputImage=file_path_output_images
                        )
                        
                        # Ambil frame pertama dari perulangan lalu simpan di variabel dan skip (lanjutkan ke frame berikut)
                        if data_blocks_first_image[component_name] is None:
                            # --- Setup bagian 4qmv Dataset ---
                            # Inisialisasi data untuk setiap blok dan setiap kuadran dengan nilai sesuai sum_data_by_quadran
                            # for quadrant in quadran_dimensions:
                            #     for feature in frames_data_quadran_column:
                            #         # Buat nama kolom dengan menggunakan template yang diberikan
                            #         column_name = f"{component_name}_{feature}_{quadrant}"
                            #         # Set value sum_data_by_quadran[feature][quadrant] ke frame_data_quadran sesuai column_name nya
                            #         frame_data_quadran[column_name] = sum_data_by_quadran[feature][quadrant]

                            # --- Setup bagian Nilai Fitur Dataset ---
                            # Inisialisasi data untuk setiap blok
                            # for i in range(total_blocks_components[component_name]):
                                # Tambahkan data ke frame_data sesuai dengan indexnya
                                # frame_data[f'X{i+1}'] = 0
                                # frame_data[f'Y{i+1}'] = 0
                                # frame_data[f'Tetha{i+1}'] = 0
                                # frame_data[f'Magnitude{i+1}'] = 0
                                # # Tambahkan data ke frame_data_all_component sesuai dengan indexnya
                                # frame_data_all_component[f'{component_name}-X{i+1}'] = 0
                                # frame_data_all_component[f'{component_name}-Y{i+1}'] = 0
                                # frame_data_all_component[f'{component_name}-Tetha{i+1}'] = 0
                                # frame_data_all_component[f'{component_name}-Magnitude{i+1}'] = 0

                            # Append data frame ke list frames_data sesuai dengan component_name
                            frames_data[component_name].append(frame_data)
                            # Tambahkan kolom "Folder Path" dengan nilai folder saat ini
                            frame_data['Folder Path'] = "data_test"
                            # Tambahkan kolom "Label" dengan nilai label saat ini
                            frame_data['Label'] = "data_test"
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

                        # plt.quiver(quivData[:, 0], quivData[:, 1], quivData[:, 2], quivData[:, 3], scale=1, scale_units='xy', angles='xy', color="r")    

                        # # num = 0
                        # for rect_def in valPOC[2]:
                        #     x, y, width, height = rect_def
                            
                        #     rects = patches.Rectangle((x,y), width,height, edgecolor='r', facecolor='none') 
                        #     plt.gca().add_patch(rects)
                            
                        #     # plt.text(x,y,f'({num})', color="blue") 
                        #     # num += 1

                        # Pemanggilan class untuk mengeluarkan nilai karakteristik vektor
                        # blok ke, x,y,tetha, magnitude, dan quadran ke
                        initQuadran = Quadran(quivData) 
                        quadran = initQuadran.getQuadran()

                        # print(tabulate(quadran, headers=['Blok Ke', 'X', 'Y', 'Tetha', 'Magnitude', 'Quadran Ke']))
                        # plt.axis('on') 
                        # plt.show() 

                        # Update frame_data dengan data quadran
                        for i, quad in enumerate(quadran):
                            # --- Setup bagian Nilai Fitur Dataset ---
                            # Set data kedalam frame_data sesuai column nya
                            frame_data[f'X{i+1}'] = quad[1]
                            frame_data[f'Y{i+1}'] = quad[2]
                            frame_data[f'Tetha{i+1}'] = quad[3]
                            frame_data[f'Magnitude{i+1}'] = quad[4]

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
                        
                        # --- Setup bagian Nilai Fitur Dataset ---
                        # Append data frame ke list
                        frames_data[component_name].append(frame_data)
                        # Tambahkan kolom "Folder Path" dengan nilai folder saat ini
                        frame_data['Folder Path'] = "data_test"
                        # Tambahkan kolom "Label" dengan nilai label saat ini
                        frame_data['Label'] = "data_test"

                        # --- Setup bagian 4qmv Dataset ---
                        # Inisialisasi data untuk setiap blok dan setiap kuadran dengan nilai sesuai sum_data_by_quadran
                        for quadran in quadran_dimensions:
                            for feature in frames_data_quadran_column:
                                # Buat nama kolom dengan menggunakan template yang diberikan
                                column_name = f"{component_name}_{feature}_{quadran}"
                                # Set value sum_data_by_quadran[feature][quadran] ke frame_data_quadran sesuai column_name nya
                                frame_data_quadran[column_name] = sum_data_by_quadran[feature][quadran]

                        current_image_data["components"][component_name] = {
                            "url": image_url
                        }

                if not index[component_name] == 0:
                    # --- Setup bagian 4qmv Dataset ---
                    # Append data frame ke list frames_data_quadran untuk 4qmv
                    frames_data_quadran.append(frame_data_quadran)
                    # Tambahkan kolom "Folder Path" dengan nilai folder saat ini
                    frame_data_quadran['Folder Path'] = "data_test"
                    # Tambahkan kolom "Label" dengan nilai label saat ini
                    frame_data_quadran['Label'] = "data_test"

                    # --- Setup bagian frames data all component Dataset ---
                    # Append data frame ke list frames_data_quadran untuk 4qmv
                    frames_data_all_component.append(frame_data_all_component)
                    # Tambahkan kolom "Folder Path" dengan nilai folder saat ini
                    frame_data_all_component['Folder Path'] = "data_test"
                    # Tambahkan kolom "Label" dengan nilai label saat ini
                    frame_data_all_component['Label'] = "data_test"

                # Update index per component_name
                index[component_name] += 1

                # Append current_image_data ke output_data
                output_data.append(current_image_data)

        # Load model svm_model.joblib disini
        svm_model_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_MODEL'], 'svm_model.joblib')
        label_encoder_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_MODEL'], 'label_encoder.joblib')
        svm_model = joblib.load(svm_model_path)
        label_encoder = joblib.load(label_encoder_path)
        
        # Initialisasi dataframe dengan pandas
        df_fitur_all = pd.DataFrame(frames_data_all_component)
        except_feature_columns = ['Frame', 'Folder Path', 'Label']  
        
        # Hapus kolom except_feature_columns dari df_fitur_all
        df_fitur_all = df_fitur_all.drop(columns=except_feature_columns)

        # Lakukan prediksi dengan model yang telah dimuat
        predictions = svm_model.predict(df_fitur_all.values)

        # Ubah prediksi numerik menjadi label asli
        decoded_predictions = label_encoder.inverse_transform(predictions)
        
        result_prediction, list_predictions = get_calculate_from_predict(decoded_predictions)

        # Return response sukses untuk date video dan images, dan prediction
        return response.success(200, 'Ok', {
            "video": {"url":file_path_video.replace('\\', '/'), "name" : new_filename_with_extension},
            "result" : result_prediction,
            "list_predictions" : list_predictions,
            "images": output_data,
            "prediction": decoded_predictions.tolist()
        })
    except Exception as e:
        return response.error(message=str(e))
