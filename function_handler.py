import time

import Run_Deconvolution
from Generate_PSF import generate_1D_psf, generate_2D_psf
from Run_Deconvolution import RL_1D_Deconvolve


def psfGen1D(sigma, pixel, output, psf_gen):
    psf = generate_1D_psf(sigma, pixel, output, psf_gen)
    return psf


def psfGen2D(sigma, pixel, output, psf_gen):
    psf = generate_2D_psf(sigma, pixel, output, psf_gen)
    return psf


def decon_1D(psf_gen, mult, itera, sigma, pixel, filename, psf, output, label, out_name):
    psf = psfGen1D(sigma, pixel, output, psf_gen)
    if mult:
        iter = []
        min = 1
        while min <= itera:
            iter.append(min)
            min += 1
        for x in iter:
            start = time.time()
            print("a")
            RL_1D_Deconvolve(x, sigma, pixel, filename, psf, output, mult, label, out_name)
            end = time.time()
            print("ab")

    elif not mult:
        print("a")
        RL_1D_Deconvolve(itera, sigma, pixel, filename, psf, output, mult, label, out_name)


def decon_2D_gray(psf_gen, mult, itera, sigma, pixel, filename, output, label, out_name):
    psf = psfGen2D(sigma, pixel, output, psf_gen)
    if mult:
        iter = []
        min = 1
        while min <= itera:
            iter.append(min)
            min += 1
        for x in iter:
            start = time.time()
            print("a")
            Run_Deconvolution.RL_2D_deconvolve(x, sigma, pixel, filename, psf, output, mult, label, out_name)
            end = time.time()
            print("ab")

    elif not mult:
        print("a")
        Run_Deconvolution.RL_2D_deconvolve(itera, sigma, pixel, filename, psf, output, mult, label, out_name)


def decon_2D_color(psf_gen, mult, itera, sigma, pixel, filename, output, label, out_name):
    psf = psfGen2D(sigma, pixel, output, psf_gen)
    if mult:
        iter = []
        min = 1
        while min <= itera:
            iter.append(min)
            min += 1
        for x in iter:
            start = time.time()
            print("a")
            Run_Deconvolution.RL_Color_Deconvolution(x, sigma, pixel, filename, psf, output, mult, label, out_name)
            end = time.time()
            print("ab")

    elif not mult:
        print("a")
        Run_Deconvolution.RL_Color_Deconvolution(itera, sigma, pixel, filename, psf, output, mult, label, out_name)
