### CHEKCK THE ANNOTATIONS ####
import os
import cv2
import xml.etree.ElementTree as ET
import os
import sys
import uuid
from pathlib import Path

import yaml
from yaml.loader import SafeLoader

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH


def draw_bounding_boxes(u_id, image_folder, annotation_folder, output_folder):

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(image_folder):

        if filename.endswith('.jpg') or filename.endswith('.JPG') or filename.endswith('.png'):
            image_path = os.path.join(image_folder, filename)
            annotation_path = os.path.join(annotation_folder, f"{os.path.splitext(filename)[0]}.xml")
            if not os.path.isfile(annotation_path):
                continue

            image = cv2.imread(image_path)
            tree = ET.parse(annotation_path)
            root = tree.getroot()

            for obj in root.iter('object'):
                class_name = obj.find('name').text

                bbox = obj.find('bndbox')
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)

                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(image, class_name, (xmin, ymin - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            output_path = os.path.join(output_folder, f"annotated_{filename}")
            cv2.imwrite(output_path, image)

    return([True, output_folder])



if __name__ == "__main__":

    # Provide the path to the folder containing the images
    image_folder = 'D:/Neom/img_patches/'

    # Provide the path to the folder containing the annotations
    annotation_folder = 'D:/Neom/xml_patches/'

    # Provide the path to the output folder where annotated images will be saved
    output_folder = 'D:/Neom/anno/'

    # Draw bounding boxes on the images in the folder and save the annotated images
    draw_bounding_boxes(image_folder, annotation_folder, output_folder)
