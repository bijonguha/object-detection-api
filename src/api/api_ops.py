from enum import Enum


class ResponseCodes(Enum):

    # success codes
    SUCCESS = {"200": None}

    ERRORS_400 = {"code": 400, "400_xml": "issue with xml file"}

    ERRORS_404 = {
        "code": 404,
        "404_img": "image not found",
        "404_pairs": "pairs not found",
        "404_loc_prod": "location/product group not found",
        "404_label": "Label Type not found",
        "404_graph": "directory graph couldnot be found",
    }

    ERRORS_406 = {
        "code": 406,
        "406_match_fail": "image matching failed",
        "406_logo_fail": "logo matching failed",
        "406_inv_img": "invalid image name in product group folder",
        "406_bad_img": "bad image encountered",
    }

    ERRORS_415 = {"code": 415, "415_img": "invalid image file"}
