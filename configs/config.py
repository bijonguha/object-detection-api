import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    version: str = "V-1"
    app_name: str = "Object-Detection-Pipeline"
    base_path: str = os.getcwd()
    local_path: str = None
    api_files_folder: str = "received_files"
    logs_folder: str = "logs_folder"
    pytest_report: str = "pytest_report"
    models_folder: str = "models"
    image_slices_yaml: str = os.path.join('configs', 'image_slice.yaml')
    resample_slices_yaml: str = os.path.join('configs', 'resample_slice.yaml')
    voc_to_yolo_yaml: str = os.path.join('configs', 'voc_to_yolo.yaml')
    
settings = Settings()
