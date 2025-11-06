# backend/config.py

import os

# Define the project root path. This file is independent, avoiding circular imports.
# Assumes this file is inside the directory you want to be the ROOT (e.g., the 'backend' folder).
# If your project structure is project_root/main.py and project_root/backend/config.py, 
# you might need to go up one level: os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Given your previous traceback showed E:\Shopsmart\backend\main.py, we assume the 'backend' folder
# is the working root for paths relative to the code.
PATH_ROOT = os.path.dirname(os.path.abspath(__file__)) 

# Define ML Model Paths using the root
# Assumes structure: backend/ml/price_trend_model.joblib
ML_FOLDER_PATH = os.path.join(PATH_ROOT, "ml")
ENCODER_PATH = os.path.join(ML_FOLDER_PATH, "platform_encoder.joblib")
MODEL_PATH = os.path.join(ML_FOLDER_PATH, "price_trend_model.joblib")