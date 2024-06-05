import math
import tqdm
import pydicom
import glob
import matplotlib.pyplot as plt
import cv2
import random

sample_count = 5
base_x, base_y = 512, 512

dcm_files = glob.glob(r"C:\Users\ragom\PycharmProjects\DICOM-Kidney-Segmentation\C4KC-KiTS\C4KC-KiTS\**\**\*-Segmentation-*\*.dcm", recursive=True)

'''
y_scale_max, x_scale_max = 1e9, 1e9
for i in tqdm.tqdm(dcm_idx_subset):
    dcm_data = pydicom.dcmread(dcm_files[i])
    if hasattr(dcm_data, 'PixelSpacing'):
        dcm_pixel_ratios = dcm_data.PixelSpacing
        y_scale, x_scale = 1/dcm_pixel_ratios[0], 1/dcm_pixel_ratios[1]
        if y_scale < y_scale_max:
            y_scale_max = y_scale
        if x_scale < x_scale_max:
            x_scale_max = x_scale

uniform_shape = [int(math.ceil(512*x_scale)), int(math.ceil(512*y_scale))]
'''

count = 0
for dcm in tqdm.tqdm(dcm_files):
    count += 1

    dcm_data = pydicom.dcmread(dcm)
    dcm_idx_subset = random.sample(range(dcm_data.NumberOfFrames), sample_count)

    '''
    if hasattr(dcm_data, 'PixelSpacing'):
        dcm_pixel_ratios = dcm_data.PixelSpacing
        y_scale, x_scale = 1/dcm_pixel_ratios[0], 1/dcm_pixel_ratios[1]
    '''

    image_arr1 = dcm_data.SegmentSequence[0].pixel_array
    image_arr2 = dcm_data.SegmentSequence[1].pixel_array


    for idx in dcm_idx_subset:
        image_arr1 = dcm_data.SegmentSequence[idx]['pixel_array']
        image_arr2 = dcm_data.SegmentSequence[idx]['pixel_array']

        f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
        ax1.imshow(image_arr1, cmap=plt.cm.bone)
        ax2.imshow(image_arr2, cmap=plt.cm.bone)

        plt.show()



    '''
    if y_scale:
        image_arr = cv2.resize(image_arr, dsize=(int(512*x_scale), int(512*y_scale)), interpolation=cv2.INTER_CUBIC)
        left_pad = int(math.floor(image_arr.shape[1]-uniform_shape[1] / 2))
        right_pad = int(math.ceil(image_arr.shape[1]-uniform_shape[1] / 2))
        top_pad = int(math.floor(image_arr.shape[0]-uniform_shape[0] / 2))
        bottom_pad = int(math.ceil(image_arr.shape[0]-uniform_shape[0] / 2))
        image_arr = cv2.copyMakeBorder(image_arr, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=0)
    '''


test = 0