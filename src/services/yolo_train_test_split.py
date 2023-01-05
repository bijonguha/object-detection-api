import os
import shutil
from pathlib import Path
import random
import math
from tqdm import tqdm
import sys

FILE = Path(__file__).resolve()
ROOT = FILE.parents[2]  # project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH

from src.utils.utilities import make_directories

img_dir = Path(r'D:\BijonGuha\Projects\object-detection\data\processed\180yolo_c270e14d130f45a1a9b9a1a391daf316\dataset\images').as_posix()
anno_dir = Path(r'D:\BijonGuha\Projects\object-detection\data\processed\180yolo_c270e14d130f45a1a9b9a1a391daf316\dataset\labels').as_posix()
extension_image = '.jpg'

ratio = 0.20

images = os.listdir(img_dir)
annos = os.listdir(anno_dir)

tmp_names_img = [im.split('.')[0] for im in images]
tmp_names_anno = [an.split('.')[0] for an in annos]

common = list(set(tmp_names_img).intersection(set(tmp_names_anno)))
random.shuffle(common)
split = math.ceil(len(common)*ratio)

test = common[0:split]
train = common[split:]

train_img_dir = os.path.join(img_dir, 'train')
test_img_dir = os.path.join(img_dir, 'val')
train_anno_dir = os.path.join(anno_dir, 'train')
test_anno_dir = os.path.join(anno_dir, 'val')

dir_list = [train_img_dir, test_img_dir, train_anno_dir, test_anno_dir]
make_directories(dir_list)

print("Len train labels :", len(train))
for tr in tqdm(train, desc='Training sets restructuring'):
    shutil.move(os.path.join(img_dir, tr+extension_image), train_img_dir)
    shutil.move(os.path.join(anno_dir, tr+'.txt'), train_anno_dir)

print("Len Val labels :", len(test))
for tr in tqdm(test, desc="Validation sets restructuring"):
    shutil.move(os.path.join(img_dir, tr+extension_image), test_img_dir)
    shutil.move(os.path.join(anno_dir, tr+'.txt'), test_anno_dir)

print("Completed")
