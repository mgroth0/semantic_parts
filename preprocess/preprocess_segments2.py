import json
import os

from PIL import Image
import numpy as np
import cv2

data_folder = '../data/Real Object Drawings/data/'
segments_folder = data_folder + 'segments/'
all_folder = data_folder + 'all/'
segment_data2_folder = data_folder + 'segment_data2/'
os.makedirs(segment_data2_folder, exist_ok=True)

DEBUG = None


def ceildiv(a, b):
    return -(-a // b)


pictures = dict()

for category in os.listdir(segments_folder):
    if category == '.DS_Store': continue
    cat_folder = segments_folder + category + '/'
    for im_file in os.listdir(cat_folder):
        if DEBUG is not None and (category + '/' + im_file) != DEBUG: continue
        full_im_file = cat_folder + im_file
        all_cat_fold = all_folder + category + '/'
        is_all_file = 'All' in im_file
        all_im_file = all_cat_fold + im_file
        if is_all_file:
            os.rename(full_im_file, all_im_file)
        else:
            segment_data_cat_fold = segment_data2_folder + category + '/'
            os.makedirs(segment_data_cat_fold, exist_ok=True)
            data_file = segment_data_cat_fold + ''.join(im_file.split('_')[:-1]) + '.json'

            im_id = im_file[0:2]
            print(f"{im_id=}")
            if im_id not in pictures:
                pictures[im_id] = [data_file]
            pictures[im_id].append(full_im_file)

segment_data = dict()
debug_json = json.dumps(pictures)
print(f"${debug_json=}")
debug_keys = list(pictures.keys())
print(f"{debug_keys=}")
print(f"{len(debug_keys)=}")
print(f"{debug_keys[0]=}")
for k in debug_keys:
    print(f"{k=}")
    v = pictures[k]
    segment_data[k] = {
        "segments": {}
    }
for pic in pictures.keys():
    layers = pictures[pic]
    json_file = [l for l in layers if 'json' in l][0]
    segment_pic_data = segment_data[pic]
    for layer_pic in [l for l in layers if 'json' not in l]:
        print(f"{layer_pic=}")
        segment_im = Image.open(layer_pic)
        segment_im = segment_im.convert('RGB')
        segment_im = np.array(segment_im)
        print('preprocessing segments for ' + layer_pic)

        segment = []
        segment_pic_data["segments"][layer_pic.split("_L")[-1].split(".")[0]] = segment

        for row in segment_im:
            bool_row = []
            segment.append(bool_row)
            for pix in row:
                pix = pix.tolist()
                # print("pix=" + json.dumps(pix))
                white = pix[0] == 255 and pix[1] == 255 and pix[2] == 255

                bool_row.append(not white)

    with open(json_file, 'w') as f:
        f.write(json.dumps(segment_pic_data))

        # Image.fromarray(im).save(crop_file)

print("done")
