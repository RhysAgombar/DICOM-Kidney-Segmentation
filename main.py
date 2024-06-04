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
dcm_idx_subset = random.sample(range(len(dcm_files)), sample_count)

test_dcm = pydicom.dcmread(dcm_files[0])

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

count = 0
for i in tqdm.tqdm(dcm_idx_subset):
    count += 1

    dcm_data = pydicom.dcmread(dcm_files[i])
    if hasattr(dcm_data, 'PixelSpacing'):
        dcm_pixel_ratios = dcm_data.PixelSpacing
        y_scale, x_scale = 1/dcm_pixel_ratios[0], 1/dcm_pixel_ratios[1]

    image_arr = dcm_data.pixel_array
    if y_scale:
        image_arr = cv2.resize(image_arr, dsize=(int(512*x_scale), int(512*y_scale)), interpolation=cv2.INTER_CUBIC)
        left_pad = int(math.floor(image_arr.shape[1]-uniform_shape[1] / 2))
        right_pad = int(math.ceil(image_arr.shape[1]-uniform_shape[1] / 2))
        top_pad = int(math.floor(image_arr.shape[0]-uniform_shape[0] / 2))
        bottom_pad = int(math.ceil(image_arr.shape[0]-uniform_shape[0] / 2))
        image_arr = cv2.copyMakeBorder(image_arr, top_pad, bottom_pad, left_pad, right_pad, cv2.BORDER_CONSTANT, value=0)

    plt.figure()
    plt.imshow(image_arr, cmap=plt.cm.bone)

    if count % 10 == 0:
        plt.show()


test = 0