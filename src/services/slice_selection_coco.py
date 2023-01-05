import json
import shutil
import os
from random import sample
from math import ceil

from tqdm import tqdm
from pycocotools.coco import COCO

from pathlib import Path
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from src.utils.utilities import make_directories

coco_anno_path = r'D:\BijonGuha\Projects\object-detection\runs\slice_coco\truck_coco_1500_02.json'
images_directory = r'D:\BijonGuha\Projects\object-detection\runs\slice_coco\truck_coco_images_1500_02'
json_dump_path = os.path.join('runs','sampled_truck_coco_images_1500_02', 'sampled_truck_coco_1500_02.json')
images_dump_dir = os.path.join('runs','sampled_truck_coco_images_1500_02','images')
sample_ratio = 1

make_directories([images_dump_dir])

coco = COCO(coco_anno_path)

imageids_with_objects = list(set([item['image_id'] for key,item in coco.anns.items()]))
filtered_images_dict = {k:v for k,v in coco.imgs.items() if v['id'] in imageids_with_objects}
rejected_images_dict = {k:v for k,v in coco.imgs.items() if v['id'] not in imageids_with_objects}

sampled_coco = {}
sampled_coco['images'] = [v for k,v in filtered_images_dict.items()]
sampled_coco['annotations'] = [v for k,v in coco.anns.items()]
sampled_coco['categories'] = [v for k,v in coco.cats.items()]

print("Annotations Sampled")
with open(json_dump_path, 'w', encoding='utf-8') as f:
    json.dump(sampled_coco, f, ensure_ascii=False, indent=4)
print('JSON Dumped into {%s} file' %json_dump_path)

filtered_images_names = [v['file_name'] for k,v in filtered_images_dict.items()]
rejected_images_names = [v['file_name'] for k,v in rejected_images_dict.items()]
combined_list = []

if len(filtered_images_names) > len(rejected_images_names):
    combined_list = filtered_images_names + rejected_images_names
else:
    samp_len = ceil(sample_ratio * len(filtered_images_names))
    combined_list = filtered_images_names + sample(rejected_images_names, samp_len)

print('Object Images : %d, Combined Images : %d' %(len(filtered_images_names), len(combined_list)))

for im in tqdm(combined_list, desc='Transferring Images'):
    shutil.copy(os.path.join(images_directory, im), images_dump_dir)

