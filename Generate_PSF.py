import math
import os

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

def generate_1D_psf(sigma, pixels, output, psf_gen):
    Xval = []
    min = 1
    max = pixels
    Xo = pixels / 2

    while min <= max:
        Xval.append(min)
        min += 1

    psf = []
    psfimg = []
    for X in Xval:
        results = ((1 / (math.sqrt(2 * math.pi * sigma))) *
                   (math.pow(math.e, -(math.pow((X - Xo), 2) / (2 * math.pow(sigma, 2))))))
        psf.append(results)
        total = ((results * (2 * math.pi * math.pow(sigma, 2))) * 100)
        psfimg.append(total)
    if psf_gen:
        plt.plot(psfimg)
        name = "psf" + str(sigma) + ".tif"
        tmp = name
        if os.path.isfile(tmp):
            os.remove(tmp)
        plt.savefig("{}/{}".format(output, name))
    psf = np.array(psf, dtype=np.float32)
    return psf


def generate_2D_psf(sigma, pixels, output, psf_gen):
    Xval = []
    min = 1
    max = pixels

    while min <= max:
        Xval.append(min)
        min += 1

    Yval = Xval
    Yo = pixels / 2
    Xo = pixels / 2
    psf = []
    psfimg = []
    for X in Xval:
        for Y in Yval:
            results = ((1 / (2 * math.pi * math.pow(sigma, 2))) *
                       (math.pow(math.e, -(math.pow((X - Xo), 2) / (2 * math.pow(sigma, 2))))) *
                       (math.pow(math.e, -(math.pow((Y - Yo), 2) / (2 * math.pow(sigma, 2))))))
            psf.append(results)
            total = ((results * (2 * math.pi * math.pow(sigma, 2))) * 100)
            psfimg.append(total)
    if psf_gen:
        array = np.reshape(psfimg, (pixels, pixels))
        psf = np.reshape(psf, (pixels, pixels))
        data = Image.fromarray(array)
        plt.imshow(data)
        name = "psf" + str(sigma) + ".tif"
        tmp = name
        if os.path.isfile(tmp):
            os.remove(tmp)
        data.save("{}/{}".format(output, name))

    psf = np.array(psf, dtype=np.float32)
    return psf
