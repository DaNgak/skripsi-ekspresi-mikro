COMPONENTS_SETUP = {
    'mulut': {
        'object_name': 'mouth',
        'object_rectangle': {"x_right": 54, "x_left": 48, "y_highest": 52, "y_lowest": 57},
        'pixel_shifting': {"pixel_x": 25, "pixel_y": 5},
        'object_dimension': {'width': 139, 'height': 39}
    },
    'mata_kiri': {
        'object_name': 'eye_left',
        'object_rectangle': {"x_right": 39, "x_left": 36, "y_highest": 38, "y_lowest": 40},
        'pixel_shifting': {"pixel_x": 20, "pixel_y": 15},
        'object_dimension': {'width': 81, 'height': 43}
    },
    'mata_kanan': {
        'object_name': 'eye_right',
        'object_rectangle': {"x_right": 45, "x_left": 42, "y_highest": 43, "y_lowest": 47},
        'pixel_shifting': {"pixel_x": 20, "pixel_y": 15},
        'object_dimension': {'width': 81, 'height': 43}
    },
    'alis_kiri': {
        'object_name': 'eyebrow_left',
        'object_rectangle': {"x_right": 21, "x_left": 17, "y_highest": 18, "y_lowest": 21},
        'pixel_shifting': {"pixel_x": 15, "pixel_y": 5},
        'object_dimension': {'width': 111, 'height': 28}
    },
    'alis_kanan': {
        'object_name': 'eyebrow_right',
        'object_rectangle': {"x_right": 26, "x_left": 22, "y_highest": 25, "y_lowest": 22},
        'pixel_shifting': {"pixel_x": 15, "pixel_y": 5},
        'object_dimension': {'width': 111, 'height': 28}
    }
}

BLOCKSIZE = 7
MODEL_PREDICTOR = "shape_predictor_68_face_landmarks.dat"
MODEL_SVM_EXTRACTION_FEATURE = "svm_model.joblib"
MODEL_SVM_EXTRACTION_FEATURE = "label_encoder.joblib"
MODEL_SVM_4QMV = "svm_model_4qmv.joblib"
QUADRAN_DIMENSIONS = ['Q1', 'Q2', 'Q3', 'Q4']
FRAMES_DATA_QUADRAN_COMPONENTS = ['sumX', 'sumY', 'Tetha', 'Magnitude', 'JumlahQuadran']
