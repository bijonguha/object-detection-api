import os
import json
import argparse
from tqdm import tqdm

def save_coco(filename, images, annotations, categories):
    '''
    Save coco json file
    '''
    with open(filename, 'wt', encoding='UTF-8') as coco:
        json.dump({'images': images, 'annotations': annotations, 
                    'categories': categories}, coco, indent=4, sort_keys=True)
    print('Generated filename :', filename)

def main(annotations_path):
    '''
    Correct file names in coco annotation
    '''
    annotations_path = annotations_path.as_posix()
    ## Think about a decorator function to check path sanity

    try:
        with open(annotations_path, 'rt', encoding='UTF-8') as annotations:
            coco = json.load(annotations)
    except Exception as e:
        print(f'Json file loading failed - {e}')
        return ([False, e])

    images = coco['images']
    annotations = coco['annotations']
    categories = coco['categories']

    for img in tqdm(images):
        tmp = img['file_name']
        tmp = os.path.basename(tmp)
        img['file_name'] = tmp

    print('Correction Completed')
    
    filename = annotations_path.replace('.json', '_corrected.json')
    
    try:
        save_coco(filename, images, annotations, categories)
    except Exception as e:
        print('Corrected JSON file creation failed ', e)
        return[False, e]

    return [True, filename]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Correct COCO annotations file_name')
    parser.add_argument('annotations_path', metavar='coco_annotations', type=str,
                        help='Path to COCO annotations file.')
    args = parser.parse_args()

    main(args.annotations_path)

    ##Ex - python .\src\services\coco_correct_filenames.py test_coco_vehicles.json