import argparse

from pycocotools.coco import COCO

from pathlib import Path

def main(annotations_path):
    '''
    Generate labels.txt from coco annotation files
    '''
    coco = COCO(annotations_path)

    cat_dict = coco.cats #capturing coco categories
    cat_list = []
    for key,item in cat_dict.items():
        cat_list.append(item['name'])
    
    if (len(cat_list) > 0):

        filename = Path(annotations_path).parent / 'labels.txt'

        with open(filename.as_posix(), 'w') as f:
            f.write('\n'.join(cat_list))

        print('Categories generated : ', cat_list)
        print('Location : ',filename)
        return [True, filename]

    else:

        print('No categories found')
        return [False, 'No categories found']

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Generate label txt from coco annotations')
    parser.add_argument('annotations_path', metavar='coco_annotations', type=str,
                        help='Path to COCO annotations file.')
    args = parser.parse_args()

    main(args.annotations_path)