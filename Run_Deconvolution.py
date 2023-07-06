import os
from multiprocessing import Pool
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from skimage import color, restoration
import time
import numpy as np
import File_Attributes as fa


def RL_2D_deconvolve(iterations, sigma, pixels, file, psf, output_path, mult_img, label):
    # Image input and setup
    print(output_path)
    blurred_img = os.path.basename(os.path.normpath(file))
    print(blurred_img)
    img_input = file
    img = mpimg.imread(img_input)
    size = fa.size(img_input)
    w = (size[0]) / 100
    h = (size[1]) / 100
    img_grey = color.rgb2gray(img)
    print("Original Image Dimension is\nHeight = {} pixels\nWidth = {} pixels"
          .format(size[0], size[1]))

    # Generate PSF and run RL Deconvolution
    print(mult_img)
    if mult_img:
        start = time.time()
        itera = []
        min = 1
        while min <= iterations:
            itera.append(min)
            min += 1

        for x in itera:
            deconvolved_RL = restoration.richardson_lucy(img_grey, psf, num_iter=x)
            # Create image output
            plt.gray()
            name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(x) + \
                "sig" + str(sigma) + ".tif"
            plt.figure(figsize=(w, h), dpi=100)
            plt.axis('off')
            if label:
                plt.xlabel("{} Iterations Richardson Lucy".format(x))
            plt.imshow(deconvolved_RL)
            plt.savefig('{}/{}'.format(output_path, name), dpi=100)
            plt.close()
            end = time.time()
            print("Iteration with RL{} completed\nRun toke {} seconds".format(x, end - start))
    elif not mult_img:
        start = time.time()
        deconvolved_RL = restoration.richardson_lucy(img_grey, psf, num_iter=iterations)
        # Create image output
        plt.gray()
        name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(iterations) + \
            "sig" + str(sigma) + ".tif"
        plt.figure(figsize=(w, h), dpi=100)
        plt.axis('off')
        if label:
            plt.xlabel("{} Iterations Richardson Lucy".format(iterations))
        plt.imshow(deconvolved_RL)
        tmp = name
        if os.path.isfile(tmp):
            os.remove(tmp)
        plt.savefig('{}/{}'.format(output_path, name), dpi=100)
        plt.close()
        end = time.time()
        print("Iteration with RL{} completed\nRun toke {} seconds".format(iterations, end - start))


def RL_1D_Deconvolve(iterations, sigma, pixels, file, psf, output_path, mult_img, label):
    # Spectra input file format as (199.89	8.00) for multiple lines
    f = open('{}'.format(file), 'r')
    start = time.time()
    spectra = []
    xaxis = []
    for line in f:
        line = line.strip().split('\t')
        spectra.append(line[1])
        xaxis.append(float(line[0]))

    spectra = np.array(spectra, dtype=np.float32)
    print(spectra)
    f.close()

    if mult_img:
        itera = []
        min = 1
        while min <= iterations:
            itera.append(min)
            min += 1

        for x in itera:
            deconvolved_RL = restoration.richardson_lucy(spectra, psf, num_iter=x)
            plt.plot(deconvolved_RL)
            if label:
                plt.xlabel("{} Iterations Richardson Lucy".format(x))
            plt.xticks(xaxis)
            name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(x) + \
                "sig" + str(sigma) + ".tif"
            plt.savefig('{}/{}'.format(output_path, name))
            end = time.time()
            print("Iteration with RL{} completed\nRun toke {} seconds".format(x, end - start))

    elif not mult_img:
        start = time.time()
        deconvolved_RL = restoration.richardson_lucy(spectra, psf, num_iter=iterations)
        plt.plot(deconvolved_RL)
        if label:
            plt.xlabel("{} Iterations Richardson Lucy".format(iterations))
        plt.xticks(xaxis)
        name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(iterations) + \
            "sig" + str(sigma) + ".tif"
        tmp = name
        if os.path.isfile(tmp):
            os.remove(tmp)
        plt.savefig('{}/{}'.format(output_path, name))
        end = time.time()
        print("Iteration with RL{} completed\nRun toke {} seconds".format(iterations, end - start))


def call_run(self):
    s = time.time()
    with Pool(8) as p:
        min_iter = 1
        max_iter = 5
        print(p.map(self.RL_2D_deconvolve, range(min_iter, max_iter)))
    e = time.time()
    print("Runtime was {}".format((e - s)))
