import os
from enum import Enum


class Constants(Enum):

    VERSION = "C-1"
    SAHI_MODEL_PATH = os.path.join('logs', 'yolo_logs', 'train', '_replace_', 'weights', 'best.pt')
    IMAGE_EXTENSION = '.jpg'
    MLFLOW_LOGS_FOLDER = os.path.join('logs','mlflow')