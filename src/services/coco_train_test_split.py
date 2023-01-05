import json
import funcy
from sklearn.model_selection import train_test_split
import os

def save_coco(filename, images, annotations, categories):
    with open(filename, 'wt', encoding='UTF-8') as coco:
        json.dump({'images': images, 'annotations': annotations, 
                    'categories': categories}, coco, indent=4, sort_keys=True)
    print('Generated filename :', filename)

def filter_annotations(annotations, images):
    image_ids = funcy.lmap(lambda i: int(i['id']), images)
    return funcy.lfilter(lambda a: int(a['image_id']) in image_ids, annotations)

def main(annotations_path, split_ratio, having_annotations=False):
    with open(annotations_path, 'rt', encoding='UTF-8') as annotations:
        coco = json.load(annotations)

    images = coco['images']
    annotations = coco['annotations']
    categories = coco['categories']

    number_of_images = len(images)

    images_with_annotations = funcy.lmap(lambda a: int(a['image_id']), annotations)

    if having_annotations:
        images = funcy.lremove(lambda i: i['id'] not in images_with_annotations, images)

    x, y = train_test_split(images, train_size=split_ratio)

    filename_annotation = os.path.split(annotations_path)[-1].split('.json')[0]
    train_name = os.path.join(os.path.split(annotations_path)[0],'train_'+filename_annotation+'.json')
    test_name = os.path.join(os.path.split(annotations_path)[0],'test_'+filename_annotation+'.json')

    save_coco(train_name, x, filter_annotations(annotations, x), categories)
    print('Train COCO Json generated')
    save_coco(test_name, y, filter_annotations(annotations, y), categories)
    print('Test COCO Json generated')

    print("Saved {} entries in {} and {} in {}".format(len(x), train_name, len(y), test_name))
    return [True, train_name, len(x), test_name, len(y)]

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(description='Splits COCO annotations file into training and test sets.')
    parser.add_argument('annotations_path', metavar='coco_annotations', type=str,
                        help='Path to COCO annotations file.')
    parser.add_argument('-s', dest='split', type=float, default=0.80,
                        help="A percentage of a split; a number in (0, 1)")
    parser.add_argument('--having-annotations', dest='having_annotations', action='store_true',
                        help='Ignore all images without annotations. Keep only these with at least one annotation')

    args = parser.parse_args()

    main(args.annotations_path, args.split, args.having_annotations)