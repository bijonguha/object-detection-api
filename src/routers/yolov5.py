from __future__ import annotations
from cgitb import reset
from unittest import result
import uu
import uuid
from click import UUID
import pdb
import os

from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

from src.api_data_models.data_models import (YoloAnotRequest, 
                                            YoloAnotResponse, 
                                            YoloDetectRequest, 
                                            YoloDetectResponse, 
                                            YoloTrainRequest, 
                                            YoloTrainResponse)

# from src.external_packages.yolov5 import train_custom

# from src.services.voc_to_yolo import main as vty_main

from src.constants import Constants

router = APIRouter()

@router.post("/annotation/", 
            tags=["Train - YOLOV5"],
            summary= "Convert Pascal VOC annotation to YOLO Format",
            response_model=YoloAnotResponse,
            response_model_exclude_none=True)
async def generate_yolo_files(vty_args : YoloAnotRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    

    # resp = vty_main(u_id, vty_args.directory_with_xmlfiles, 
    #                     vty_args.directory_with_imgfiles)

    # if resp[0]:
    #     sucs_msg = {'status' : 'success', 'code' : 200,
    #                 'u_id' : u_id, 'directory_with_yolofiles': resp[1]
    #     }
    #     response_dict.update(sucs_msg)
    #     return response_dict
    # else:
    #     fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
    #     response_dict.update(fail_msg)
    #     return response_dict

@router.post("/train/", 
            tags=["Train - YOLOV5"],
            summary= "Trains yolov5 model in the dataset mentioned in config",
            response_model=YoloTrainResponse,
            response_model_exclude_none=True)
async def update_item(train_args: YoloTrainRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    
    
    os.environ['MLFLOW_LOGS_FOLDER'] = Constants.MLFLOW_LOGS_FOLDER.value

    # resp = train_custom.run(data=train_args.config_path, epochs = train_args.epochs,
    #                         batch_size = train_args.batch_size, imgsz = train_args.img_size,
    #                         resume = train_args.resume)

    # if resp[0]:
    #     sucs_msg = {'status' : 'success', 'code' : 200,
    #                 'experiment_name' : os.path.split(resp[1].save_dir)[-1]
    #     }
    #     response_dict.update(sucs_msg)
    #     return response_dict
    # else:
    #     fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
    #     response_dict.update(fail_msg)
    #     return response_dict

@router.post("/detect/", 
            tags=["Train - YOLOV5"],
            summary= "Detect using yolov5 model in the experiment folder",
            response_model=YoloDetectResponse,
            response_model_exclude_none=True)
async def update_item(train_args: YoloDetectRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    
    msg = {'status' : 'Under Development', 'code' : 200}
    response_dict.update(msg)
    return response_dict
    resp = train_custom.run(data=train_args.config_path, epochs = train_args.epochs,
                            batch_size = train_args.batch_size, imgsz = train_args.img_size,
                            resume = train_args.resume)

    if resp[0]:
        sucs_msg = {'status' : 'success', 'code' : 200,
                    'experiment_name' : os.path.split(resp[1].save_dir)[-1]
        }
        response_dict.update(sucs_msg)
        return response_dict
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
        response_dict.update(fail_msg)
        return response_dict