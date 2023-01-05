from typing import Optional, List
from pydantic import BaseModel, FilePath
import uuid

class ResponseBase(BaseModel):
    status : str
    code : int
    u_id : uuid.UUID
    error : Optional[str]

class SliceRequest(BaseModel):
    image_directory: str
    annotation_directory: str
    tile_size_width: Optional[int] = 1500
    tile_size_height: Optional[int] = 1500
    tile_overlap: Optional[float] = 0.20
    number_tiles : Optional[int] = 0

class SliceResponse(ResponseBase):
    image_path: Optional[str] = None
    annotation_path : Optional[str] = None
    coco_path : Optional[str] = None

class FilterRequest(BaseModel):
    image_directory: str
    annotation_directory: str
    positive_to_background_ratio: Optional[float] = 1.0

class FilterResponse(ResponseBase):
    image_path: Optional[str] = None
    annotation_path : Optional[str] = None
    roi_slices_count : Optional[int] = None
    background_slices_count : Optional[int] = None

class YoloTrainRequest(BaseModel):
    config_path: str
    epochs: Optional[int] = 5
    batch_size: Optional[int] = 4
    img_size: Optional[int] = 640
    resume: Optional[bool] = False

class YoloTrainResponse(ResponseBase):
    experiment_name: Optional[str] = None

class YoloDetectRequest(BaseModel):
    img_size: Optional[int] = 640

class YoloDetectResponse(ResponseBase):
    experiment_name: Optional[str] = None

class YoloAnotRequest(BaseModel):
    directory_with_xmlfiles: str
    directory_with_imgfiles: str

class YoloAnotResponse(ResponseBase):
    directory_with_yolofiles : Optional[str] = None

class SahiRequest(BaseModel):
    img_path: str
    experiment_id: str
    slice_height: Optional[int] = 1500
    slice_width: Optional[int] = 1500
    overlap: Optional[float] = 0.3
    device: Optional[str] = 'auto'
    confidence_score: Optional[float] = 0.3

class VOCPredBase(BaseModel):
    category: str
    score: float
    voc_bbox: List[int]

class ImageMeta(BaseModel):
    height: int
    width: int

class SahiResponse(ResponseBase):
    prediction: Optional[List[VOCPredBase]] = None
    metadata: Optional[ImageMeta] = None
    