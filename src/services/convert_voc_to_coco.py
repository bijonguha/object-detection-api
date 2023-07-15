from PIL import Image
import os
import xml.etree.ElementTree as ET
from tqdm import tqdm

from sahi.utils.coco import Coco, CocoCategory, CocoImage, CocoAnnotation
from sahi.utils.file import save_json

#-parent_folder
#|--annotation
#|--images
#|--coco.json

def convert_to_coco(annotations_dir, images_dir, class_list, IMAGE_EXTENSION):

    parent_dir = os.path.split(annotations_dir)[0]
    
    ann_folder_name = os.path.split(annotations_dir)[1]
    im_folder_name = os.path.split(images_dir)[1]
    
    ann_names = [i.split('.')[0] for i in os.listdir(annotations_dir)]
    im_names = [i.split('.')[0] for i in os.listdir(images_dir)]
    
    comm_names = list(set(ann_names).intersection(set(im_names)))

    coco = Coco()

    for i,cl in enumerate(class_list):
        coco.add_category(CocoCategory(id=i, name=cl))

    print("Category Mapping :", coco.category_mapping)

    inv_map = dict((v, k) for k, v in coco.category_mapping.items())

    for com_nam in tqdm(comm_names):
        xml_path = os.path.join(parent_dir, ann_folder_name, com_nam+'.xml')
        img_path = os.path.join(parent_dir, im_folder_name, com_nam+IMAGE_EXTENSION)

        width, height = Image.open(img_path).size
        coco_image = CocoImage(os.path.basename(img_path), height, width)

        mytree = ET.parse(xml_path)
        myroot = mytree.getroot()

        objects = []

        for it in myroot.findall('object'):
            bt = it.find('bndbox')
            xmin = bt.find('xmin').text
            ymin = bt.find('ymin').text
            xmax = bt.find('xmax').text
            ymax = bt.find('ymax').text
            category = it.find('name').text

            coco_image.add_annotation(
                CocoAnnotation(
                bbox=[int(xmin), int(ymin), int(xmax)-int(xmin), int(ymax)-int(ymin)],
                category_id=inv_map[category],
                category_name=category
                )
            )

        coco.add_image(coco_image)

    coco_json_file = os.path.join(os.path.dirname(os.path.abspath(annotations_dir)), 'coco.json')
    save_json(data=coco.json, save_path=coco_json_file)
    print('Coco json generated ', coco_json_file)

    return [True, coco_json_file]

if __name__ == '__main__':

    annotations_dir = r'D:\BijonGuha\Projects\object-detection\tests\artefacts\test_voc_coco\annotations'
    images_dir = r'D:\BijonGuha\Projects\object-detection\tests\artefacts\test_voc_coco\images'
    class_list = ['coastal_litter']
    IMAGE_EXTENSION = '.jpg'

    convert_to_coco(annotations_dir, images_dir, class_list, IMAGE_EXTENSION)