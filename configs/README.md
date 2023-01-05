# Configuration Files
This folder consists of configuration files for running services. These configuration files are very helpful for no code and quick turnaround results for object detection cases.

## image_slice.yaml

```
  # Configuration parameters
  keep_partial_labels : True
  ignore_empty_tiles : False 
  save_before_after_map : True

  # filepaths
  image_target_directory : ['data', 'interim','replace','images_sliced']
  annotation_target_directory : ['data', 'interim','replace','annotations_sliced']
```

## resample_slice.yaml

```
  # Configuration parameters
  positive_to_background_ratio : 1
  # filepaths
  image_target_directory : ['data', 'processed','replace','images_filtered']
  annotation_target_directory : ['data', 'processed','replace','annotations_filtered']
```

## voc_to_yolo.yaml

```
  # Configuration parameters
  labels_directory : ['data', 'processed','replace','dataset', 'labels']
  classes_path : ['data', 'processed','replace','dataset']
  err_file_path : ['data', 'processed','replace','dataset']
```

## yolov5.yaml (sample)

```
# Default dataset location is next to YOLOv5:
#   /parent
#     /dataset/images
#     /dataset/labels
#     /yolov5_train_on_UAVDT


# Train/val/test sets as 1) dir: path/to/imgs, 2) file: path/to/imgs.txt, or 3) list: [path/to/imgs1, path/to/imgs2, ..]
path: ../../../tests/artefacts/yolo_trucks  # dataset root dir
train: images/train  # train images (relative to 'path') 128 images
val: images/val  # val images (relative to 'path') 128 images
test:  # test images (optional)

# Classes
nc: 3  # number of classes
names: [ 'empty-truck', 'unwetted-truck', 'unwetted-truck' ]  # class name

# Mlflow experiment name
mlflow_exp : 'exp_yolo'
```
