### GENERATE IMAGE PATCHES FROM IMAGES AND XML ANNOTATIONS ###
import os
import cv2
import xml.etree.ElementTree as ET
import math
import sys
from tqdm import tqdm

from pathlib import Path

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from src.utils.utilities import make_directories

def generate_image_patches(image_folder, annotation_folder, patch_size, stride, min_object_size, img_out, ann_out):

    make_directories([img_out, ann_out])

    image_files = os.listdir(image_folder)
    image_files = [f for f in image_files if f.endswith(".jpg") or f.endswith(".png") or f.endswith(".JPG")]

    patch_num = 0
    count_empty = 0
    problem_files = []

    for image_file in tqdm(image_files, desc = "Generating image slices"):
        try:
            image_path = os.path.join(image_folder, image_file)
            annotation_file = os.path.join(annotation_folder, f"{os.path.splitext(image_file)[0]}.xml")

            image = cv2.imread(image_path)
            height, width, _ = image.shape

            tree = ET.parse(annotation_file)
            root = tree.getroot()

            has_objects = False

            for obj in root.iter('object'):
                has_objects = True
                break

            if not has_objects:
                # Remove the image file
                # os.remove(image_path)
                count_empty += 1
                continue

            for y in range(0, height - patch_size, stride):
                for x in range(0, width - patch_size, stride):
                    patch = image[y:y+patch_size, x:x+patch_size]

                    patch_annotations = []

                    for obj in root.iter('object'):
                        class_name = obj.find('name').text

                        bbox = obj.find('bndbox')
                        xmin = math.floor(float(bbox.find('xmin').text))
                        ymin = math.floor(float(bbox.find('ymin').text))
                        xmax = math.floor(float(bbox.find('xmax').text))
                        ymax = math.floor(float(bbox.find('ymax').text))

                        # Adjust coordinates relative to patch
                        xmin -= x
                        ymin -= y
                        xmax -= x
                        ymax -= y

                        # Discard annotations outside the patch
                        if xmax < 0 or ymax < 0 or xmin > patch_size or ymin > patch_size:
                            continue

                        # Clip coordinates to patch boundaries
                        xmin = max(0, xmin)
                        ymin = max(0, ymin)
                        xmax = min(patch_size, xmax)
                        ymax = min(patch_size, ymax)

                        object_width = xmax - xmin
                        object_height = ymax - ymin

                        # Check if object size is below the minimum threshold
                        if object_width < min_object_size or object_height < min_object_size:
                            continue

                        patch_annotations.append({
                            'class': class_name,
                            'bbox': {'xmin': xmin, 'ymin': ymin, 'xmax': xmax, 'ymax': ymax}
                        })

                    if len(patch_annotations) == 0:
                        # No object found in the patch or all objects are below the minimum size, skip generating the annotation
                        continue

                    patch_filename = f"patch_{patch_num}.jpg"
                    patch_path = os.path.join(img_out, patch_filename)
                    cv2.imwrite(patch_path, patch)

                    annotation_filename = f"patch_{patch_num}.xml"
                    annotation_path = os.path.join(ann_out, annotation_filename)

                    patch_root = ET.Element('annotation')

                    for annotation in patch_annotations:
                        obj = ET.SubElement(patch_root, 'object')
                        name = ET.SubElement(obj, 'name')
                        name.text = annotation['class']
                        bbox = ET.SubElement(obj, 'bndbox')
                        xmin = ET.SubElement(bbox, 'xmin')
                        ymin = ET.SubElement(bbox, 'ymin')
                        xmax = ET.SubElement(bbox, 'xmax')
                        ymax = ET.SubElement(bbox, 'ymax')
                        xmin.text = str(annotation['bbox']['xmin'])
                        ymin.text = str(annotation['bbox']['ymin'])
                        xmax.text = str(annotation['bbox']['xmax'])
                        ymax.text = str(annotation['bbox']['ymax'])

                    patch_tree = ET.ElementTree(patch_root)
                    patch_tree.write(annotation_path)

                    patch_num += 1
                    
        except Exception as e:
            print(f"Error processing image {image_file}: {e}")
            problem_files.append(image_file)

    print("Total number of images: ", len(image_files))    
    print("Total number of empty images: ", count_empty)
    print("Total number of patches: ", patch_num)
    print("Output folder: ", img_out)
    print("Output annotation folder: ", ann_out)
    print("Problem files: ", problem_files)


if __name__ =="__main__":
    # Provide the path to the image folder, annotation folder, patch size, stride, and output folder
    image_folder = "D:/Neom/all_sample/"
    annotation_folder = "D:/Neom/xmls/"
    patch_size = 2048  # Example patch size
    stride = 512  # Example stride
    output_folder = 'D:/Neom/img_patches/'
    min_object_size = 250  # Example minimum object size threshold

    # Generate image patches with patched annotations for images containing objects and excluding small objects
    generate_image_patches(image_folder, annotation_folder, patch_size, stride, output_folder, min_object_size)
