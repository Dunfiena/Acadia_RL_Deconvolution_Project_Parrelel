import os
import sys
from multiprocessing import Pool
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from skimage import color, restoration
import time
import numpy as np
import File_Attributes as fa


def RL_2D_deconvolve(iterations, sigma, pixels, file, psf, output_path, label):
    multproc = main_function
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
    plt.savefig('{}/{}'.format(output_path, name), dpi=100)
    plt.close()


def RL_1D_Deconvolve(iterations, sigma, pixels, file, psf, output_path, mult_img, label):
    # Spectra input file format as (199.89	8.00) for multiple lines
    f = open('{}'.format(file), 'r')
    spectra = []
    xaxis = []
    for line in f:
        line = line.strip().split('\t')
        spectra.append(line[1])
        xaxis.append(float(line[0]))

    spectra = np.array(spectra, dtype=np.float32)
    print(spectra)
    f.close()

    deconvolved_RL = restoration.richardson_lucy(spectra, psf, num_iter=iterations)

    plt.plot(xaxis, deconvolved_RL)
    if label:
        plt.xlabel("{} Iterations Richardson Lucy".format(iterations))

    name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(iterations) + \
        "sig" + str(sigma) + ".tif"
    plt.savefig('{}/{}'.format(output_path, name))


class main_function:
    def get_label(self):
        return self.label

    def get_sigma(self):
        return self.sigma

    def get_output_path(self):
        return self.output_path

    def get_psf(self):
        return self.psf

    def get_file(self):
        return self.file

    def get_pixels(self):
        return self.pixels

    def get_interations(self):
        return self.iterations

    def __init__(self):
        self.label = None
        self.output_path = None
        self.psf = None
        self.file = None
        self.pixels = None
        self.sigma = None
        self.iterations = None

    def call_run(self, iterations, sigma, pixels, file, psf, output_path, label):
        s = time.time()
        self.iterations = iterations
        self.sigma = sigma
        self.pixels = pixels
        self.file = file
        self.psf = psf
        self.output_path = output_path
        self.label = label

        with Pool(8) as p:
            min_iter = 1
            max_iter = 5
            print(p.map(RL_2D_deconvolve, range(min_iter, max_iter)))
        e = time.time()
        print("Runtime was {}".format((e - s)))
