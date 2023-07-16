from __future__ import annotations
from cgitb import reset
from unittest import result
import uu
import uuid
from click import UUID
import pdb

from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

from src.services.image_slicing import create_slices, voc_slices
from src.services.check_voc_anno import draw_bounding_boxes

from src.api_data_models.data_models import SliceRequest, SliceResponse, SliceChecker, SliceVocRequest
router = APIRouter()

@router.post("/folder_info_voc/", 
            tags=["Slicing"],
            summary= "Create VOC slices of images and annotations for object detection",
            response_model=SliceResponse,
            response_model_exclude_none=False)
async def update_item_voc(folder: SliceVocRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}

    resp = voc_slices(u_id, folder.image_directory, folder.annotation_directory,
    folder.patch_size, folder.stride, folder.min_object_size)

    if resp[0]:
        sucs_msg = {'status' : 'success', 'code' : 200,
                    'image_path' : resp[1], 'annotation_path' : resp[2]
        }
        response_dict.update(sucs_msg)
        return response_dict
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
        response_dict.update(fail_msg)
        return response_dict

@router.post("/folder_info_coco/", 
            tags=["Slicing"],
            summary= "Create COCO slices of images annotations for object detection",
            response_model=SliceResponse,
            response_model_exclude_none=True)
async def update_item_coco(folder: SliceRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}

    resp = create_slices(u_id, folder.image_directory, folder.annotation_directory,
    folder.tile_size_width, folder.tile_size_height, folder.tile_overlap,
    folder.number_tiles, type = 'coco')

    if resp[0]:
        sucs_msg = {'status' : 'success', 'code' : 200,
                    'coco_path' : resp[1] }
        response_dict.update(sucs_msg)
        return response_dict
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
        response_dict.update(fail_msg)
        return response_dict
    
@router.post("/validate_voc_annotations/", 
            tags=["Annotations Ops"],
            summary= "Validate the VOC slices of images and annotations",
            response_model=SliceResponse,
            response_model_exclude_none=True)
async def check_voc_slices(folder: SliceChecker):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}
    print("Above function")
    resp = draw_bounding_boxes(u_id, folder.image_directory, folder.annotation_directory, folder.output_directory)
    print("below function")
    print(f"--------------------------{resp}")
    if resp[0]:
        sucs_msg = {'status' : 'success', 'code' : 200,
                    'output_path' : resp[1]
        }
        response_dict.update(sucs_msg)
        return response_dict
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
        response_dict.update(fail_msg)
        return response_dict