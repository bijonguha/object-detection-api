# !mkdir checkpoint_yolof
# !mim download mmdet --config yolof_r50_c5_8x8_1x_coco --dest checkpoint_yolof

from mmdet.datasets import build_dataset
from mmdet.models import build_detector
from mmdet.apis import train_detector
import mmcv
import os.path as osp
from mmcv import Config
from mmdet.apis import set_random_seed

cfg = Config.fromfile('/content/checkpoint_yolof/yolof_r50_c5_8x8_1x_coco.py')

# Modify dataset type and path
cfg.dataset_type = 'CocoDataset'
cfg.classes = 'coastal_litter/labels.txt'
cfg.data_root = 'coastal_litter/'

cfg.data.test.type = 'CocoDataset'
cfg.data.test.classes = 'coastal_litter/labels.txt'
cfg.data.test.data_root = 'coastal_litter/'
cfg.data.test.ann_file = 'test_sampled_sliced_coco_corrected.json'
cfg.data.test.img_prefix = 'images'

cfg.data.train.type = 'CocoDataset'
cfg.data.train.classes = 'coastal_litter/labels.txt'
cfg.data.train.data_root = 'coastal_litter/'
cfg.data.train.ann_file = 'train_sampled_sliced_coco_corrected.json'
cfg.data.train.img_prefix = 'images'

cfg.data.val.type = 'CocoDataset'
cfg.data.val.classes = 'coastal_litter/labels.txt'
cfg.data.val.data_root = 'coastal_litter/'
cfg.data.val.ann_file = 'test_sampled_sliced_coco_corrected.json'
cfg.data.val.img_prefix = 'images'

# modify num classes of the model in box head
cfg.model.bbox_head.num_classes = 1
# We can still use the pre-trained Mask RCNN model though we do not need to
# use the mask branch
cfg.load_from = '/content/checkpoint_yolof/yolof_r50_c5_8x8_1x_coco_20210425_024427-8e864411.pth'
###cfg.load_from = '/content/drive/MyDrive/siemens/mmdet/yolo_coastal_litter/yolof_epoch_24.pth'
# Set up working dir to save files and logs.
cfg.work_dir = 'coastal_litter'

# Change the evaluation metric since we use customized dataset.
cfg.evaluation.metric = 'bbox'
# We can set the evaluation interval to reduce the evaluation times
cfg.evaluation.interval = 3
cfg.evaluation.save_best = 'bbox_mAP'


cfg.optimizer.lr = .015

# We can set the checkpoint saving interval to reduce the storage cost
cfg.checkpoint_config.interval = 10

cfg.log_config.interval = 1
cfg.runner.max_epochs = 40

cfg.lr_config.policy = 'step'
cfg.lr_config.step = [8,14,20,30]
# Set seed thus the results are more reproducible
cfg.seed = 0
set_random_seed(0, deterministic=False)
cfg.gpu_ids = range(1)
cfg.data.samples_per_gpu = 16
cfg.data.workers_per_gpu = 4
cfg.workflow = [('train', 1)]
cfg.log_config.hooks = [dict(type='TextLoggerHook'),
                        dict(type='TensorboardLoggerHook')
                       ]
cfg.log_level = 'INFO'
# We can initialize the logger for training and have a look
# at the final config used for training
print(f'Config:\n{cfg.pretty_text}')

with open('/content/coastal_litter/yolo_c2.py', 'w') as f:
    f.write(cfg.pretty_text)



# Build dataset
datasets = [build_dataset(cfg.data.train)]

# Build the detector
model = build_detector(
    cfg.model, train_cfg=cfg.get('train_cfg'), test_cfg=cfg.get('test_cfg'))
# Add an attribute for visualization convenience
model.CLASSES = datasets[0].CLASSES

# Create work_dir
mmcv.mkdir_or_exist(osp.abspath(cfg.work_dir))
train_detector(model, datasets, cfg, distributed=False, validate=True)