#!/bin/env python
# This script takes a folder containing images and creates a mosaic image from these
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import ImageGrid
import numpy as np
import math
import PIL
from glob import glob
import sys

def factor_int(n):
    val = math.ceil(math.sqrt(n))
    val2 = int(n/val)
    while val2 * val != float(n):
        val -= 1
        val2 = int(n/val)
    return val, val2, n

def grid_from_subplot(path, save=False, dest=None):
    imgs = glob(f"{path}/*.jpg")
    f1, f2, f3 = factor_int(len(imgs))
    fig, ax = plt.subplots(f1, f2, figsize=(10, 10), sharex=True, sharey=True)
    count=0

    for i in range(f1):
        for j in range(f2):
            im = imgs[count]
            img = PIL.Image.open(im)
            ax[i,j].imshow(img)
            count +=1
    for a in ax.ravel():
        a.set_axis_off()

    plt.tight_layout()
    plt.subplots_adjust(wspace=0.01, hspace=0.01)
    if not save:
        plt.show()
    else:
        plt.savefig(dest, bbox_inches='tight')

def img_reshape(img):
    from PIL import Image
    img = Image.open(img).convert('RGB')
    img = img.resize((300,300))
    img = np.asarray(img)
    return img

def grid_from_imggrid(path, save=False, dest=None):
    imgs = glob(f"{path}/*.jpg")
    imgs.extend(glob(f"{path}/*.jpeg"))
    imgs = sorted(imgs)
    f1, f2, f3 = factor_int(len(imgs))
    # f1 = 6
    # f2 = 2
    # print(f1,f2,f3)

    if f1>f2:
        wid = f1
        ht = f2
    else:
        wid = f2
        ht = f1

    img_arr = []
    for image in imgs:
        img_arr.append(img_reshape(image))

    fig = plt.figure(figsize=(10., 10.))
    grid = ImageGrid(fig, 111,
                     nrows_ncols=(ht, wid),  # creates 2x2 grid of axes
                     axes_pad=0.1,  # pad between axes
                     )

    for ax, im in zip(grid, img_arr):
        ax.imshow(im)
        ax.set_axis_off()

    # plt.tight_layout()
    if not save:
        plt.show()
    else:
        plt.savefig(dest, bbox_inches='tight')

if __name__=="__main__":
    folder = sys.argv[1]

    save=False
    try:
        dest = sys.argv[2]
    except:
        dest = None
    else:
        save=True
    # print(save)
    # grid_from_subplot(folder, save, dest)
    grid_from_imggrid(folder, save, dest)
