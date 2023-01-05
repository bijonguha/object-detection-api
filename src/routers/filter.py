# python libraries
import uuid
import pdb

# Installed libraries
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel

# custom modules
from src.services.slice_selection import filter_data

from src.api_data_models.data_models import FilterRequest, FilterResponse

router = APIRouter()

@router.post("/folder_path_voc/", 
            tags=["Slices Resampling for VOC data"],
            summary= "Resampling slices of images and annotations based on roi and background",
            response_model=FilterResponse,
            response_model_exclude_none=True)
async def update_item_voc(folder: FilterRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}

    resp = filter_data(u_id, folder.image_directory, folder.annotation_directory,
                        folder.positive_to_background_ratio, type='voc')

    if resp[0]:
        sucs_msg = {'status' : 'success', 'code' : 200,
                    'image_path' : resp[1], 'annotation_path' : resp[2],
                    'roi_slices_count' : resp[3], 'background_slices_count' : resp[4]
        }
        response_dict.update(sucs_msg)
        return response_dict
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
        response_dict.update(fail_msg)
        return response_dict

@router.post("/folder_path_coco/", 
            tags=["Slices Resampling for COCO data"],
            summary= "Resampling slices of images and annotations based on roi and background",
            response_model=FilterResponse,
            response_model_exclude_none=True)
async def update_item_coco(folder: FilterRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}

    resp = filter_data(u_id, folder.image_directory, folder.annotation_directory,
                        folder.positive_to_background_ratio, type='coco')

    if resp[0]:
        sucs_msg = {'status' : 'success', 'code' : 200,
                    'image_path' : resp[1], 'annotation_path' : resp[2],
                    'roi_slices_count' : resp[3], 'background_slices_count' : resp[4]
        }
        response_dict.update(sucs_msg)
        return response_dict
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'error' : resp[1]}
        response_dict.update(fail_msg)
        return response_dict