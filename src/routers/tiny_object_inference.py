import uuid
import os

from fastapi import APIRouter

from src.services.sahi_prediction import predict_sahi
from src.constants import Constants
from src.api_data_models.data_models import SahiRequest, SahiResponse, ImageMeta

router = APIRouter()

@router.post("/slice_based_yolo/", 
            tags=["Predict Slices - SAHI"],
            summary= "Preidction based of Slices using yolov5 generated model",
            response_model=SahiResponse,
            response_model_exclude_none=True)
async def update_item(sahi_args: SahiRequest):

    u_id = uuid.uuid4()
    response_dict = {'u_id' : u_id.hex}    

    generic_path = Constants.SAHI_MODEL_PATH.value
    model_path = generic_path.replace('_replace_', sahi_args.experiment_id)

    if os.path.isfile(model_path):
        try:
            resp = predict_sahi(sahi_args.img_path, model_path, sahi_args.slice_height, sahi_args.overlap,
                            sahi_args.slice_width, sahi_args.device, sahi_args.confidence_score)
            sucs_msg = {'status' : 'success', 'code' : 200, 'u_id' : u_id,
                        'prediction' : resp}
            return sucs_msg

        except Exception as e:
            fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : e}            
            return fail_msg
    
    else:
        fail_msg = {'status' : 'failed', 'code' : 400, 'u_id' : u_id, 'error' : 'invalid experiment id'}
        return fail_msg
