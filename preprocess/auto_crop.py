import os

from PIL import Image
import numpy as np

DEBUG = None
#DEBUG = 'Face/Ba_Jan2018_F_Face_FU3.png'
#DEBUG = 'House/Aa_Blu0500_M_House_CON.png'

data_folder = '../data/Real Object Drawings/data/'
raw_folder = data_folder + 'raw/'
crop_demo_folder = data_folder + 'crop_demo/'
os.makedirs(crop_demo_folder, exist_ok=True)

# THRESHOLD = 255
THRESHOLD = 100

for category in os.listdir(raw_folder):
    if category == '.DS_Store': continue
    cat_folder = raw_folder + category + '/'
    for im_file in os.listdir(cat_folder):
        if im_file == 'Labeled': continue
        if DEBUG is not None and (category + '/' + im_file) != DEBUG: continue
        crop_cat_fold = crop_demo_folder + category + '/'
        os.makedirs(crop_cat_fold, exist_ok=True)
        crop_file = crop_cat_fold + im_file

        im = Image.open(cat_folder + im_file)

        if DEBUG:
            im.show()

        im = np.array(im)

        if DEBUG:
            print(im)

        print('cropping ' + category + '/' + im_file)

        first_colored_y = None
        last_colored_y = None
        first_colored_x = None
        last_colored_x = None

        for y in range(im.shape[0]):
            row = im[y]
            colored = any(any(c < THRESHOLD for c in px) for px in row)
            if colored:
                last_colored_y = y
                if first_colored_y is None:
                    first_colored_y = y

        for x in range(im.shape[1]):
            col = im[:, x]
            colored = any(any(c < THRESHOLD for c in px) for px in col)
            if colored:
                last_colored_x = x
                if first_colored_x is None:
                    first_colored_x = x

        im[first_colored_y, :, :] = 0
        im[last_colored_y, :, :] = 0
        im[:, first_colored_x, :] = 0
        im[:, last_colored_x, :] = 0

        Image.fromarray(im).save(crop_file)
        if DEBUG:
            print(f'{first_colored_y=}')
            print(f'{last_colored_y=}')
            print(f'{first_colored_x=}')
            print(f'{last_colored_x=}')

print("done")
