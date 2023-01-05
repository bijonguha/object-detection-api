import uuid
import os
from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel, FilePath, DirectoryPath

from src.api_data_models.data_models import ResponseBase
from src.services.convert_voc_to_coco import convert_to_coco
from src.services import (coco_correct_filenames, 
                        coco_create_labeltxt, 
                        coco_train_test_split, coco_merge_annotations)

router = APIRouter()

class CocoOpsResponse(ResponseBase):
    filepath : Optional[FilePath]

class CocoOpsRequest(BaseModel):
    coco_json_path : Optional[FilePath]

class CocoToVocRequest(BaseModel):
    annotations_dir : DirectoryPath
    images_dir : DirectoryPath
    class_list : List[str]
    image_extension : str

class CocoTrainTestRequest(CocoOpsRequest):
    split_ratio : Optional[float] = 0.80

class CocoTrainTestResponse(CocoOpsResponse):
    train_filepath : FilePath
    length_train : int
    test_filepath : FilePath
    length_test : int

class CocoMergeRequest(BaseModel):
    input_extend : FilePath
    input_add : FilePath

@router.post("/voc_to_coco/", 
            tags=["COCO Data Ops"],
            summary= "Convert VOC dataset into COCO format",
            description="Dataset\n--images\n--annotations",
            response_model=CocoOpsResponse,
            response_model_exclude_none=True)
async def voc2coco(func_args: CocoToVocRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    

    try:
        resp = convert_to_coco(func_args.annotations_dir, func_args.images_dir,
                            func_args.class_list, func_args.image_extension)
        
        if resp[0]:
            sucs_msg = {'status' : 'success', 'code' : 200, 'u_id' : u_id,
                        'filepath' : resp[1]}
            return sucs_msg
        else:
            fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : resp[1]}            
            return fail_msg

    except Exception as e:
        fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : e}            
        return fail_msg

@router.post("/coco_filename_correction/", 
            tags=["COCO Data Ops"],
            summary= "Check or Correct COCO annotation filenames",
            response_model=CocoOpsResponse,
            response_model_exclude_none=True)
async def voc2coco(func_args: CocoOpsRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    

    try:
        resp = coco_correct_filenames.main(func_args.coco_json_path)
        
        if resp[0]:
            sucs_msg = {'status' : 'success', 'code' : 200, 'u_id' : u_id,
                        'filepath' : resp[1]}
            return sucs_msg
        else:
            fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : resp[1]}            
            return fail_msg

    except Exception as e:
        fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : e}            
        return fail_msg

@router.post("/generate_labels_txt/", 
            tags=["COCO Data Ops"],
            summary= "Generate labels.txt for training",
            response_model=CocoOpsResponse,
            response_model_exclude_none=True)
async def voc2coco(func_args: CocoOpsRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    

    try:
        resp = coco_create_labeltxt.main(func_args.coco_json_path)
        
        if resp[0]:
            sucs_msg = {'status' : 'success', 'code' : 200, 'u_id' : u_id,
                        'filepath' : resp[1]}
            return sucs_msg
        else:
            fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : resp[1]}            
            return fail_msg

    except Exception as e:
        fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : e}            
        return fail_msg

@router.post("/create_coco_train_test_split/", 
            tags=["COCO Data Ops"],
            summary= "Create two coco json for training and testing",
            response_model=CocoTrainTestResponse,
            response_model_exclude_none=True)
async def voc2coco(func_args: CocoTrainTestRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}

    try:
        resp = coco_train_test_split.main(func_args.coco_json_path,
                                            func_args.split_ratio)
        
        if resp[0]:
            sucs_msg = {'status' : 'success', 'code' : 200, 'u_id' : u_id,
                        'train_filepath' : resp[1], 'length_train' : resp[2],
                        'test_filepath' : resp[3], 'length_test' : resp[4]}
            return sucs_msg
        else:
            fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : resp[1]}            
            return fail_msg

    except Exception as e:
        fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : e}            
        return fail_msg

@router.post("/merge_coco_annotation/", 
            tags=["COCO Data Ops"],
            summary= "Create combined coco from two others",
            response_model=CocoOpsResponse,
            response_model_exclude_none=True)
async def coco_merge(func_args: CocoMergeRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    

    try:
        resp = coco_merge_annotations.coco_merge(func_args.input_extend, func_args.input_add)
        
        if resp[0]:
            sucs_msg = {'status' : 'success', 'code' : 200, 'u_id' : u_id,
                        'filepath' : resp[1]}
            return sucs_msg
        else:
            fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : resp[1]}            
            return fail_msg

    except Exception as e:
        fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : e}            
        return fail_msg