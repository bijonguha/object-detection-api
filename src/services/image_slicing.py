# default libraries
import os
import sys
import uuid
from pathlib import Path

# installed libraries
import yaml
from yaml.loader import SafeLoader

import image_bbox_slicer as ibs
from sahi.slicing import slice_coco

from src.services.voc_slicer import generate_image_patches

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from configs.config import settings

def voc_slices(u_id, image_directory, annotation_directory,
                patch_size, stride, min_object_size,
                config_path=settings.image_slices_yaml):
    '''
    Function to create slices of image and bounding box annotation using
    slicing yaml file in configs
    '''

    rand_str = u_id.hex

    # Open the file and load the file
    with open(config_path) as f:
        slice_config = yaml.load(f, Loader=SafeLoader)

    im_dst = os.path.join(*slice_config['image_target_directory']).replace('replace', rand_str)
    an_dst = os.path.join(*slice_config['annotation_target_directory']).replace('replace', rand_str)

    im_src = Path(image_directory).as_posix()
    an_src = Path(annotation_directory).as_posix()

    if not (os.path.isdir(im_src)):
        print("Invalid Image directory path passed")
        return[False,"Invalid Image directory path passed"]

    if not (os.path.isdir(an_src)):
        print("Invalid Annotation directory path passed")
        return[False,"Invalid Annotation directory path passed"]

    print("Process Started")

    try:
        generate_image_patches(im_src, an_src, patch_size, stride, min_object_size, im_dst, an_dst)
        
    except Exception as e:
        print(f'exception occured in voc slicing- {e}')
        return ([False, e])

    print("Process Successfully Completed")
    
    print("Folder name generated : ", im_dst)

    return([True, im_dst, an_dst])


def coco_slicing(u_id, image_directory, annotation_file_path, tile_size_width=1500,
                        tile_size_height=1500, tile_overlap=0.20,
                        config_path=settings.image_slices_yaml):

    rand_str = u_id.hex

    # Open the file and load the file
    with open(config_path) as f:
        slice_config = yaml.load(f, Loader=SafeLoader)

    im_dst = os.path.join(*slice_config['coco_data_dir']).replace('replace', rand_str)
    an_dst = os.path.join(*slice_config['annotation_path']).replace('replace', rand_str)
    coco_json_filename = 'sliced'

    try:
        coco_dict, coco_path = slice_coco(
            coco_annotation_file_path=annotation_file_path,
            image_dir=image_directory,
            output_coco_annotation_file_name=os.path.join('..',coco_json_filename),
            ignore_negative_samples=slice_config["ignore_negative_samples"],
            output_dir=im_dst,
            slice_height=tile_size_width,
            slice_width=tile_size_height,
            overlap_height_ratio=tile_overlap,
            overlap_width_ratio=tile_overlap,
            min_area_ratio=0.1,
            verbose=False
        )
        print('Slices generated at ,', im_dst)

        return [True, im_dst]

    except Exception as e:
        print('Coco slicing failed due to ',e)
        return [False, e]

def create_slices(u_id, image_directory, annotation_directory, tile_size_width=1500,
                     tile_size_height=1500, tile_overlap=0.20, number_tiles=0,
                     config_path=settings.image_slices_yaml, type = 'voc'):

    if type == 'voc':
        return voc_slices(u_id, image_directory, annotation_directory, tile_size_width,
                        tile_size_height, tile_overlap, number_tiles,
                        config_path=settings.image_slices_yaml)

    if type == 'coco':
        return coco_slicing(u_id, image_directory, annotation_directory, tile_size_width,
                        tile_size_height, tile_overlap,
                        config_path=settings.image_slices_yaml)
    

from sahi.slicing import slice_coco

if __name__ == '__main__':

    image_directory = r'tests\artefacts\test_voc_coco\images'
    annotation_directory = r'tests\artefacts\test_voc_coco\annotations'
    annotation_path = r'tests\artefacts\test_voc_coco\coco.json'
    import uuid
    create_slices(uuid.uuid4(), image_directory, annotation_path, type='coco')