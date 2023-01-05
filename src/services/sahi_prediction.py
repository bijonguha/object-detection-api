import torch
from sahi.model import Yolov5DetectionModel
from sahi.utils.cv import read_image
from sahi.predict import get_prediction, get_sliced_prediction

def predict_sahi(img, model_path, slice_height = 1500, slice_width=1500, overlap = 0.3,
                 device = 'auto', conf_thresh=0.3):

    yolov5_model_path = model_path

    if device == 'auto':
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'

    detection_model = Yolov5DetectionModel(
        model_path=yolov5_model_path,
        confidence_threshold=conf_thresh,
        device=device
    )

    result = get_sliced_prediction(
        img,
        detection_model,
        slice_height = slice_height,
        slice_width = slice_width,
        overlap_height_ratio = overlap,
        overlap_width_ratio = overlap
    )

    result.export_visuals(export_dir="logs/sahi_predictions/")
    print("Image saved : logs/sahi_predictions/prediction_visual.png")
    
    res_list = []

    for i,res in enumerate(result.object_prediction_list):
        res_list.append({'category' : res.category.name,
                        'score': res.score.value,
                        'voc_bbox': res.bbox.to_voc_bbox()})

    print('time taken :',result.durations_in_seconds)

    res_dict = {'predictions':res_list}

    return res_dict

if __name__ == '__main__':
    img = r'D:\BijonGuha\Projects\object-detection-neom\tests\artefacts\sahi_test_truck\0a7307a2-DJI_20220120103424_0198.JPG'
    model_path = r'D:\BijonGuha\Projects\object-detection-neom\tests\artefacts\sahi_test_truck\best.pt'

    predict_sahi(img, model_path)