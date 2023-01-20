# python libraries
import pdb
import os, sys
from shutil import copyfile
import random
import math
from math import ceil
from cv2 import split
import json
from random import sample

# installed libraries
from joblib import Parallel, delayed
from matplotlib.font_manager import json_dump
from tqdm import tqdm
from tqdm.contrib import tzip
import cv2
import numpy as np
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET
from pycocotools.coco import COCO
from pathlib import Path
import shutil

import yaml
from yaml.loader import SafeLoader

# custom modules
from src.utils.utilities import parse_xml_voc, make_directories
from src.utils.utilities import make_directories

from configs.config import settings

def validate_xml(xml_path):
    name, boxes = parse_xml_voc(xml_path)
    if len(boxes)>0:
        return True
    return False

sep_name = lambda x : os.path.split(x)[-1].split('.xm')[0]

def filter_data_voc(u_id, jpg_data_dir, xml_data_dir, ratio = 1, 
            config_path=settings.resample_slices_yaml):

    rand_str = u_id.hex

    # Open the file and load the file
    with open(config_path) as f:
        filter_config = yaml.load(f, Loader=SafeLoader)

    filter_jpg_dir = os.path.join(*filter_config['image_target_directory']).replace('replace', rand_str)
    filter_xml_dir = os.path.join(*filter_config['annotation_target_directory']).replace('replace', rand_str)

    make_directories([filter_jpg_dir, filter_xml_dir])

    ratio = filter_config['positive_to_background_ratio']

    tmp_files = os.listdir(xml_data_dir)
    files_xml = [os.path.join(xml_data_dir,f) for f in tmp_files if '.xml' in f]

    if len(files_xml)<1:
        return [False, "not found any xml files"]

    tmp_files = os.listdir(jpg_data_dir)
    files_img = [os.path.join(jpg_data_dir,f) for f in tmp_files if '.jpg' in f]

    if len(files_img)<1:
        return [False, "not found any jpg files"]    

    print("Total data count :", len(files_xml))

    xml_roi = [xml for xml in files_xml if validate_xml(xml)]
    print("ROI object counts :",len(xml_roi))

    if len(xml_roi)<1:
        return [False, "not found any xml file with roi"]

    name_roi = [sep_name(xml) for xml in xml_roi]
    xml_background = list(set(files_xml).difference(set(xml_roi)))
    random_background = []
    
    if len(xml_background) > 0:
        name_background = [sep_name(xml) for xml in xml_background]
        len_split = math.ceil(len(name_roi) * ratio)
        random_background = random.sample(name_background, len_split)
        print("Background counts :", len(random_background))
        names = name_roi + random_background

    else:
        print("Sampling is not required as all images have roi object")
        names = name_roi    

    print("ROI object counts :",len(name_roi))

    # to copy xml annotations in filter folder
    xml_paths = [os.path.join(xml_data_dir, name+'.xml') for name in names]
    xml_filter_paths = [os.path.join(filter_xml_dir, name+'.xml') for name in names]

    # to copy jpg images in filter folder
    jpg_paths = [os.path.join(jpg_data_dir, name+'.jpg') for name in names]
    jpg_filter_paths = [os.path.join(filter_jpg_dir, name+'.jpg') for name in names]

    src_list = xml_paths+jpg_paths
    tar_list = xml_filter_paths+jpg_filter_paths

    [copyfile(src,tar) for src,tar in tzip(src_list, tar_list)]

    return [True, filter_jpg_dir, filter_xml_dir, len(name_roi), len(random_background)]


def filter_data_coco(u_id, jpg_data_dir, coco_path, ratio = 1, 
            config_path=settings.resample_slices_yaml):
    
    rand_str = u_id.hex

    images_directory = jpg_data_dir
    coco_anno_path = coco_path
    sample_ratio = ratio

    with open(config_path) as f:
        filter_config = yaml.load(f, Loader=SafeLoader)

    images_dump_dir = os.path.join(*filter_config['coco_data_dir']).replace('replace', rand_str)
    tmp_json_dump_path = os.path.join(*filter_config['annotation_path']).replace('replace', rand_str)
    json_dump_path = os.path.join(tmp_json_dump_path, 'sampled_'+os.path.basename(coco_anno_path))

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
        samp_len = math.ceil(sample_ratio * len(filtered_images_names))
        combined_list = filtered_images_names + sample(rejected_images_names, samp_len)

    print('Object Images : %d, Combined Images : %d' %(len(filtered_images_names), len(combined_list)))

    for im in tqdm(combined_list, desc='Transferring Images'):
        shutil.copy(os.path.join(images_directory, im), images_dump_dir)

    print('Images transferred at : ', images_dump_dir)
    
    return[True, images_dump_dir, json_dump_path, len(filtered_images_names), len(combined_list)-len(filtered_images_names)]


def filter_data(u_id, jpg_data_dir, anno_path, ratio, 
            config_path=settings.resample_slices_yaml, type = 'voc'):
    
    if type == 'voc':
        return filter_data_voc(u_id, jpg_data_dir, anno_path, ratio, 
            config_path=settings.resample_slices_yaml)
    
    elif type == 'coco':
        return filter_data_coco(u_id, jpg_data_dir, anno_path, ratio, 
            config_path=settings.resample_slices_yaml)