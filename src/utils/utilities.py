# python libraries
import os
import shutil
import xml.etree.ElementTree as ET

# installed libraries
import filetype

def make_directories(dir_list):
    for _dir_ in dir_list:
        if os.path.exists(_dir_):
            continue
        os.makedirs(_dir_)


def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


def clean_dir(dir_list):
    for _dir_ in dir_list:
        if os.path.exists(_dir_):
            shutil.rmtree(_dir_)

def check_filetype(filepath, types):
    """
    Function for checking file types

    Parameters
    ----------
    filepath : str
    type : list or str of MIME types

    Returns
    -------
    res : Boolean(True / False)
    """
    kind = filetype.guess(filepath)

    if isinstance(types, list):
        if kind and kind.mime in types:
            return True
    else:
        if kind and types == kind.mime:
            return True

    return False

def parse_xml_voc(xml_file: str):
    '''
    Parse pascal voc annotation
    '''

    if not os.path.isfile(xml_file):
        print("XML not found")
        return None

    tree = ET.parse(xml_file)
    root = tree.getroot()

    list_with_all_boxes = []
    filename = root.find('filename').text

    for boxes in root.iter('object'):

        ymin, xmin, ymax, xmax = None, None, None, None

        ymin = int(boxes.find("bndbox/ymin").text)
        xmin = int(boxes.find("bndbox/xmin").text)
        ymax = int(boxes.find("bndbox/ymax").text)
        xmax = int(boxes.find("bndbox/xmax").text)

        list_with_single_boxes = [xmin, ymin, xmax, ymax]
        list_with_all_boxes.append(list_with_single_boxes)

    return filename, list_with_all_boxes