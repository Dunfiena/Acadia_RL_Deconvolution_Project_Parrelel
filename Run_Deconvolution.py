import os
import sys
import cv2
import matplotlib.pyplot as plt
from matplotlib import image as mpimg
from skimage import color, restoration
import numpy as np
import File_Attributes as fa


def RL_Color_Deconvolution(iterations, sigma, pixels, file, psf, output_path, label, out_file, mult_img):
    plt.clf()
    # Image input and setup
    print(output_path)
    blurred_img = os.path.basename(os.path.normpath(file))
    print(blurred_img)
    img_input = file
    img = cv2.imread(file)
    blue = img[:, :, 0]
    green = img[:, :, 1]
    red = img[:, :, 2]
    size = fa.size(img_input)
    w = (size[0]) / 100
    h = (size[1]) / 100

    print("Original Image Dimension is\nHeight = {} pixels\nWidth = {} pixels"
          .format(size[0], size[1]))

    print('red')
    im_red = restoration.richardson_lucy(red, psf, num_iter=iterations, clip=False)
    print('blue')
    im_blue = restoration.richardson_lucy(blue, psf, num_iter=iterations, clip=False)
    print('green')
    im_green = restoration.richardson_lucy(green, psf, num_iter=iterations, clip=False)

    if out_file != file:
        name = out_file + ".png"
        if mult_img:
            name = out_file + "({})".format(iterations) + ".png"
    else:
        name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(iterations) +\
            "sig" + str(sigma) + ".png"
    im_dec = cv2.merge([im_blue, im_green, im_red])
    im_dec = np.array(im_dec)
    im_deca = im_dec.astype(int)
    cv2.imwrite('{}/{}'.format(output_path, name), im_deca)
    return name

def RL_2D_deconvolve(iterations, sigma, pixels, file, psf, output_path, label, out_file, mult_img):
    plt.clf()
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
    name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(iterations) + "sig" + str(sigma) + ".png"
    plt.figure(figsize=(w, h), dpi=100)
    plt.axis('off')
    if label:
        plt.xlabel("{} Iterations Richardson Lucy".format(iterations))
    plt.imshow(deconvolved_RL)
    plt.savefig('{}/{}'.format(output_path, name), dpi=100)
    return name

def RL_1D_Deconvolve(iterations, sigma, pixels, file, psf, output_path, mult_img, label, out_file):
    plt.clf()
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
    print("a")
    print(psf)
    deconvolved_RL = restoration.richardson_lucy(spectra, psf, num_iter=iterations, clip=False)
    print("c")
    plt.plot(deconvolved_RL)
    if label:
        plt.xlabel("{} Iterations Richardson Lucy".format(iterations))

    name = os.path.basename(os.path.normpath(file)) + " " + "pixel" + str(pixels) + "RL" + str(iterations) + \
         "sig" + str(sigma) + ".png"
    i = 0

    with open('{}/{}.txt'.format(output_path, name), 'w') as f:
        for _ in xaxis:
            f.write('{}   {}\n'.format(xaxis[i], deconvolved_RL[i]))
            i = i + 1
    plt.savefig('{}/{}'.format(output_path, name))
    return name
