import matplotlib.pyplot as plt
import numpy as np
import math
import tqdm
import pydicom
import glob
import matplotlib.pyplot as plt
import cv2
import random

sample_count = 5
base_z, base_x, base_y = 1222, 512, 512
scale_factor = 20
resized_3d_img = np.zeros((base_z, int(base_x/scale_factor), int(base_y/scale_factor)))

dcm_files = glob.glob(r"C:\Users\ragom\PycharmProjects\DICOM-Kidney-Segmentation\C4KC-KiTS\C4KC-KiTS\**\**\*-Segmentation-*\*.dcm", recursive=True)

'''
def midpoints(x):
    sl = ()
    for _ in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return x

# prepare some coordinates, and attach rgb values to each
r, g, b = np.indices((1222, 512, 512)) / 512.0
rc = midpoints(r)
gc = midpoints(g)
bc = midpoints(b)

# define a sphere about [0.5, 0.5, 0.5]
sphere = (rc - 0.5)**2 + (gc - 0.5)**2 + (bc - 0.5)**2 < 0.5**2

# combine the color components
colors = np.zeros(sphere.shape + (3,))
colors[..., 0] = rc
colors[..., 1] = gc
colors[..., 2] = bc

# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(r, g, b, sphere,
          facecolors=colors,
          linewidth=0.5)
ax.set(xlabel='r', ylabel='g', zlabel='b')
ax.set_aspect('equal')

plt.show()
'''


for dcm in tqdm.tqdm(dcm_files):
    dcm_data = pydicom.dcmread(dcm)
    image_arr = dcm_data.pixel_array

    for idx in range(image_arr.shape[0]):
        img = image_arr[idx, :, :]
        img_sm = cv2.resize(img, (resized_3d_img.shape[1], resized_3d_img.shape[2]), interpolation=cv2.INTER_CUBIC)
        resized_3d_img[idx, :, :] = img_sm

    voxels = resized_3d_img > 0
    sub_vox = voxels[::scale_factor,:,:]

    ax = plt.figure().add_subplot(projection='3d')
    ax.voxels(filled=sub_vox,
              linewidth=0.5)
    ax.set(xlabel='r', ylabel='g', zlabel='b')
    ax.set_aspect('equal')

    plt.show()
