from app import response, app
from flask import url_for
from werkzeug.utils import secure_filename
import uuid, os, datetime, dlib, cv2
from app.request.DataModel.DataTestStoreRequest import DataTestStoreRequest
from app.helper.preprocessing import get_frames_by_input_video, extract_component_by_images, draw_quiver_and_save_plotlib_image, convert_video_to_webm
from app.helper.helper import convert_video_to_avi, natural_sort_key, get_calculate_from_predict
from app.helper.poc import POC
from app.helper.vektor import Vektor
from app.helper.quadran import Quadran
from app.helper.constant import COMPONENTS_SETUP, FRAMES_DATA_QUADRAN_COMPONENTS, MODEL_PREDICTOR, MODEL_SVM_4QMV, MODEL_SVM_EXTRACTION_FEATURE , QUADRAN_DIMENSIONS, BLOCKSIZE
import joblib
import pandas as pd

def testing():
    # request_data = DataTestStoreRequest()
    
    # if not request_data.validate():
    #     return response.error(422, 'Invalid request form validation', request_data.errors)
    
    try:
        # Set path folder input video
        input_video_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'data-test', 'casme')

        # Initialize an empty list to store data entries
        results_list = []
        with_preview = False

        # Initialize variables for setup testing
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_MODEL'], MODEL_PREDICTOR))
        components_setup = COMPONENTS_SETUP
        quadran_dimensions = QUADRAN_DIMENSIONS
        frames_data_quadran_column = FRAMES_DATA_QUADRAN_COMPONENTS
        total_blocks_components = {component_name: 0 for component_name in components_setup}
        data_blocks_first_image = {component_name: None for component_name in components_setup}
        index = {component_name: 0 for component_name in components_setup}

        for component_name, component_info in components_setup.items():
            total_blocks_components[component_name] = int((component_info['object_dimension']['width'] / BLOCKSIZE) * (component_info['object_dimension']['height'] / BLOCKSIZE))

        # Loop through all folders in the input video folder
        for folder_name in os.listdir(input_video_folder):
            folder_path = os.path.join(input_video_folder, folder_name)
            if os.path.isdir(folder_path):
                for video_name in os.listdir(folder_path):
                    video_path = os.path.join(folder_path, video_name)

                    # If the path is not a directory, skip this loop
                    if not os.path.isdir(video_path):
                        continue

                    # Reset variables for each new video folder
                    data_blocks_first_image = {component_name: None for component_name in components_setup}
                    index = {component_name: 0 for component_name in components_setup}
                    frames_data_quadran = []
                    frames_data_all_component = []

                    for filename in sorted(os.listdir(video_path), key=natural_sort_key):
                        if filename.endswith(".jpg") or filename.endswith(".png"): 
                            image = cv2.imread(os.path.join(video_path, filename))
                            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                            rects = detector(gray)

                            frame_data_all_component = {'Frame': f"{index[component_name] + 1}({filename.split('.')[0]})"}
                            frame_data_quadran = {'Frame': f"{index[component_name] + 1}({filename.split('.')[0]})"}

                            for rect in rects:
                                shape = predictor(gray, rect)
                                for component_name, component_info in components_setup.items():
                                    sum_data_by_quadran = {column: {quadrant: 0 for quadrant in quadran_dimensions} for column in frames_data_quadran_column}
                                    data_blocks_image_current, image_url = extract_component_by_images(
                                        image=image,
                                        shape=shape,
                                        frameName=filename.split(".")[0], 
                                        objectName=component_info['object_name'],
                                        objectRectangle=component_info['object_rectangle'],
                                        pixelShifting=component_info['pixel_shifting'],
                                        objectDimension=component_info['object_dimension'],
                                        directoryOutputImage=os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_IMAGE'], 'output', video_path),
                                        withPreview=False
                                    )

                                    if data_blocks_first_image[component_name] is None:
                                        data_blocks_first_image[component_name] = data_blocks_image_current
                                        continue

                                    initPOC = POC(data_blocks_first_image[component_name], data_blocks_image_current, BLOCKSIZE) 
                                    valPOC = initPOC.getPOC() 

                                    initQuiv = Vektor(valPOC, BLOCKSIZE)
                                    quivData = initQuiv.getVektor() 

                                    initQuadran = Quadran(quivData) 
                                    quadran = initQuadran.getQuadran()

                                    for i, quad in enumerate(quadran):
                                        frame_data_all_component[f'{component_name}-X{i+1}'] = quad[1]
                                        frame_data_all_component[f'{component_name}-Y{i+1}'] = quad[2]
                                        frame_data_all_component[f'{component_name}-Tetha{i+1}'] = quad[3]
                                        frame_data_all_component[f'{component_name}-Magnitude{i+1}'] = quad[4]

                                        if quad[5] in quadran_dimensions:
                                            sum_data_by_quadran['sumX'][quad[5]] += quad[1]
                                            sum_data_by_quadran['sumY'][quad[5]] += quad[2]
                                            sum_data_by_quadran['Tetha'][quad[5]] += quad[3]
                                            sum_data_by_quadran['Magnitude'][quad[5]] += quad[4]
                                            sum_data_by_quadran['JumlahQuadran'][quad[5]] += 1


                                    for quadran in quadran_dimensions:
                                        for feature in frames_data_quadran_column:
                                            column_name = f"{component_name}_{feature}_{quadran}"
                                            frame_data_quadran[column_name] = sum_data_by_quadran[feature][quadran]

                                # print("Frame data all component",frame_data_all_component)

                            if not index[component_name] == 0:
                                frame_data_quadran['Folder Path'] = 'data_test'
                                frame_data_quadran['Label'] = 'data_test'
                                frames_data_quadran.append(frame_data_quadran)

                                frame_data_all_component['Folder Path'] = 'data_test'
                                frame_data_all_component['Label'] = 'data_test'
                                frames_data_all_component.append(frame_data_all_component)
                                
                            index[component_name] += 1


                    # output_csv_dir = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_DATA'], video_path)
                    # os.makedirs(output_csv_dir, exist_ok=True)
                    # ambil data pertama saja dari df_fitur_all

                    df_fitur_all = pd.DataFrame(frames_data_all_component)
                    # df_fitur_all.to_csv(os.path.join(output_csv_dir, 'nilai-fitur-all-component.csv'), index=False, float_format=None)

                    df_quadran = pd.DataFrame(frames_data_quadran)
                    # df_quadran.to_csv(os.path.join(output_csv_dir, '4qmv-all-component.csv'), index=False, float_format=None)
                                
                    base_model_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_MODEL'])
                    except_feature_columns = ['Frame', 'Folder Path', 'Label']

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

                    predictions_result_all = {}
                    for train_model_key, train_model_data in model_variabel_set.items():
                        predictions_result_all[train_model_key] = {}
                        for metode_key, metode_data in train_model_data.items():
                            df = metode_data['data']
                            model_path = metode_data['model_path']
                            except_columns = metode_data['except_feature_columns']
                            label_encoder_path = metode_data['label_encoder_path']

                            df = df.drop(columns=except_columns)
                            # print('df', df.head(1))
                            # print('model_path', model_path)
                            # print('label_encoder_path', label_encoder_path)
                            svm_model = joblib.load(model_path)
                            label_encoder = joblib.load(label_encoder_path)

                            predictions = svm_model.predict(df.values)
                            decoded_predictions = label_encoder.inverse_transform(predictions)

                            result_prediction, list_predictions = get_calculate_from_predict(decoded_predictions)

                            predictions_result_all[train_model_key][metode_key] = {
                                "decoded_predictions": decoded_predictions,
                                "result_prediction": result_prediction,
                                "list_predictions": list_predictions,
                            }

                    data_entry = {
                        "Video Name": video_name,
                        "Folder Label Seharusnya": folder_name,
                    }

                    for train_model_key in model_variabel_set.keys():
                        for metode_key in model_variabel_set[train_model_key].keys():
                            key_name = f"{metode_key}_with_{train_model_key}"
                            data_entry[f"{key_name} result_predictions"] = predictions_result_all[train_model_key][metode_key]['result_prediction']
                            data_entry[f"{key_name} list_predictions"] = str(predictions_result_all[train_model_key][metode_key]['list_predictions'])

                    results_list.append(data_entry)

        # Save results dataframe to an Excel file
        results_df = pd.DataFrame(results_list)
        dir_result_prediction = os.path.join(app.config['UPLOAD_FOLDER'], 'testing')
        os.makedirs(dir_result_prediction, exist_ok=True)
        results_df.to_excel(os.path.join(dir_result_prediction, 'predictions_results_all_label_dengan_kfold.xlsx'), index=False)
        return response.success(200, f"Predictions saved to 'predictions_results.xlsx'")

    except Exception as e:
        return response.error(message=str(e))
    
# def process_videos_from_folder(input_folder):
#     output_data = []

#     for folder_name in os.listdir(input_folder):
#         folder_path = os.path.join(input_folder, folder_name)
#         if os.path.isdir(folder_path):
#             for video_file in os.listdir(folder_path):
#                 if video_file.endswith(('.avi', '.mp4', '.mkv', '.webm')):
#                     video_file_path = os.path.join(folder_path, video_file)

#                     # Process each video file
#                     result = process_single_video(video_file_path, folder_name)
#                     output_data.append(result)

#     # Convert the collected data into a DataFrame
#     df = pd.DataFrame(output_data)
    
#     # Save the DataFrame to an Excel file
#     output_excel_path = os.path.join(input_folder, 'output_predictions.xlsx')
#     df.to_excel(output_excel_path, index=False)
    
#     return output_excel_path

# def process_single_video(video_file_path, label_sebenarnya):
#     try:
#         file_extension = video_file_path.split('.')[-1].lower()
#         new_filename = f'video-{str(uuid.uuid4())}'
#         new_filename_with_extension = f"{new_filename}.{file_extension}"
#         file_path_video = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], new_filename_with_extension)
#         file_path_output_images = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_IMAGE'], 'output', new_filename)

#         # Save video ke folder di lokal
#         shutil.copy(video_file_path, file_path_video)

#         if file_extension != 'avi':
#             converted_avi_filename = f"{new_filename}.avi"
#             converted_avi_file_path = os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_VIDEO'], converted_avi_filename)
#             convert_video_to_avi(file_path_video, converted_avi_file_path)
#             os.remove(file_path_video)
#             file_path_video = converted_avi_file_path
#             new_filename_with_extension = converted_avi_filename

#         with app.app_context():
#             file_path_video_response = url_for('static', filename=file_path_video.replace('\\', '/').replace('assets/', '', 1), _external=True)

#         images, error = get_frames_by_input_video(file_path_video, file_path_output_images, 200)
#         if error is not None:
#             return response.error(message=error)

#         # Variabel untuk format response sukses output
#         output_data = []

#         # Proses perhitungan POC dan deteksi wajah
#         # (Implementasi ini diambil dari kode yang disediakan sebelumnya, sesuaikan dengan fungsi-fungsi yang ada)

#         # Mengumpulkan data frame hasil prediksi
#         output_csv_dir = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], app.config['UPLOAD_FOLDER_DATA'], new_filename))
#         os.makedirs(output_csv_dir, exist_ok=True)

#         # Setup model_variabel_set untuk prediksi
#         model_variabel_set = {
#             "random_sampling": {
#                 "fitur_all_component": {
#                     "data": df_fitur_all,
#                     "model_path": os.path.join(base_model_path, 'svm_model_random_sampling.joblib'),
#                     "except_feature_columns": except_feature_columns,
#                     "label_encoder_path": os.path.join(base_model_path, 'label_encoder_random_sampling.joblib')
#                 },
#                 "4qmv_all_component": {
#                     "data": df_quadran,
#                     "model_path": os.path.join(base_model_path, '4qmv_svm_model_random_sampling.joblib'),
#                     "except_feature_columns": except_feature_columns,
#                     "label_encoder_path": os.path.join(base_model_path, '4qmv_label_encoder_random_sampling.joblib')
#                 }
#             },
#             "kfold": {
#                 "fitur_all_component": {
#                     "data": df_fitur_all,
#                     "model_path": os.path.join(base_model_path, 'svm_model_kfold.joblib'),
#                     "except_feature_columns": except_feature_columns,
#                     "label_encoder_path": os.path.join(base_model_path, 'label_encoder_kfold.joblib')
#                 }
#             }
#         }

#         # Setup response data prediction untuk di return json
#         response_data = {
#             "video": {
#                 "url": file_path_video_response,
#                 "name": new_filename_with_extension,
#             },
#         }

#         predictions_result_all = {}
#         for train_model_key, train_model_data in model_variabel_set.items():
#             predictions_result_all[train_model_key] = {}
#             for metode_key, metode_data in train_model_data.items():
#                 df = metode_data['data']
#                 model_path = metode_data['model_path']
#                 except_columns = metode_data['except_feature_columns']
#                 label_encoder_path = metode_data['label_encoder_path']

#                 df = df.drop(columns=except_columns)

#                 svm_model = joblib.load(model_path)
#                 label_encoder = joblib.load(label_encoder_path)

#                 predictions = svm_model.predict(df.values)
#                 decoded_predictions = label_encoder.inverse_transform(predictions)

#                 result_prediction, list_predictions = get_calculate_from_predict(decoded_predictions)

#                 predictions_result_all[train_model_key][metode_key] = {
#                     "decoded_predictions": decoded_predictions,
#                     "result_prediction": result_prediction,
#                     "list_predictions": list_predictions,
#                 }

#         data_entry = {
#             "Video name": video_file_path,
#             "Folder video": label_sebenarnya,
#         }

#         for train_model_key in model_variabel_set.keys():
#             for metode_key in model_variabel_set[train_model_key].keys():
#                 key_name = f"{metode_key}_with_{train_model_key}"
#                 data_entry[f"{key_name} result_predictions"] = predictions_result_all[train_model_key][metode_key]['result_prediction']
#                 data_entry[f"{key_name} list_predictions"] = str(predictions_result_all[train_model_key][metode_key]['list_predictions'])

#         return data_entry

#     except Exception as e:
#         return {"Video name": video_file_path, "Folder video": label_sebenarnya, "error": str(e)}

# # Call the function with the desired input folder
# input_folder = 'path/to/your/input/folder'
# output_excel = process_videos_from_folder(input_folder)
# print(f"Output Excel file is saved at: {output_excel}")