import csv
import itertools
from collections import defaultdict

import cv2
import numpy as np


# get input array
def getInputArr(path, width, height):
    try:
        # read the image
        img = cv2.imread(path, 1)
        # resize it
        img = cv2.resize(img, (width, height))
        # input must be float type
        img = img.astype(np.float32)

        # since the odering of TrackNet  is 'channels_first', so we need to change the axis
        img = np.rollaxis(img, 2, 0)
        return img

    except Exception as e:

        print(path, e)


# get output array
def getOutputArr(path, nClasses, width, height):

    seg_labels = np.zeros((height, width, nClasses))
    try:
        img = cv2.imread(path, 1)
        img = cv2.resize(img, (width, height))
        img = img[:, :, 0]

        for c in range(nClasses):
            seg_labels[:, :, c] = (img == c).astype(int)

    except Exception as e:
        print(e)

    seg_labels = np.reshape(seg_labels, (width * height, nClasses))
    return seg_labels


# read input data and output data
def InputOutputGenerator(
    images_path,
    batch_size,
    n_classes,
    input_height,
    input_width,
    output_height,
    output_width,
):

    # read csv file to 'zipped'
    columns = defaultdict(list)
    with open(images_path) as f:
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            for (i, v) in enumerate(row):
                columns[i].append(v)
    zipped = itertools.cycle(zip(columns[0], columns[3]))

    while True:
        Input = []
        Output = []
        # read input&output for each batch
        for _ in range(batch_size):
            path, anno = zipped.next()
            Input.append(getInputArr(path, input_width, input_height))
            Output.append(getOutputArr(anno, n_classes, output_width, output_height))
        # return input&output
        yield np.array(Input), np.array(Output)
