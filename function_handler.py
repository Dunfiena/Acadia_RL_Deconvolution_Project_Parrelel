import time

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import Qt, QObject, pyqtSignal, QThread

import GUI_RL_Deconvolution
import Run_Deconvolution
from Generate_PSF import generate_1D_psf, generate_2D_psf
from Run_Deconvolution import RL_1D_Deconvolve, RL_2D_deconvolve, RL_Color_Deconvolution
from feedback_DS import feedback_DS as fDS

class funcThread(QThread):
    signal_1 = pyqtSignal(fDS)

    def psfGen1D(self, sigma, pixel, output, psf_gen):
        psf = generate_1D_psf(sigma, pixel, output, psf_gen)
        return psf

    def psfGen2D(self, sigma, pixel, output, psf_gen):
        psf = generate_2D_psf(sigma, pixel, output, psf_gen)
        return psf

    def decon_1D(self, psf_gen, mult, itera, sigma, pixel, filename, output, label, out_name):
        psf = self.psfGen1D(sigma, pixel, output, psf_gen)
        if mult:
            iter = []
            min = 1
            while min <= itera:
                iter.append(min)
                min += 1
            for x in iter:
                start = time.time()
                name = RL_1D_Deconvolve(x, sigma, pixel, filename, psf, output, mult, label, out_name)
                end = time.time()

                time_taken = str(end - start)
                feedback = fDS(time_taken, x, name)
                self.signal_1.emit(feedback)

        elif not mult:
            start = time.time()
            name = RL_1D_Deconvolve(itera, sigma, pixel, filename, psf, output, mult, label, out_name)
            end = time.time()

            time_taken = str(end - start)
            feedback = fDS(time_taken, itera, name)
            self.signal_1.emit(feedback)

    def decon_2D_gray(self, psf_gen, mult, itera, sigma, pixel, filename, output, label, out_name):
        psf = self.psfGen2D(sigma, pixel, output, psf_gen)
        if mult:
            iter = []
            min = 1
            while min <= itera:
                iter.append(min)
                min += 1
            for x in iter:
                start = time.time()
                name = RL_2D_deconvolve(x, sigma, pixel, filename, psf, output, mult, label, out_name)
                end = time.time()

                time_taken = str(end - start)
                feedback = fDS(time_taken, x, name)
                self.signal_1.emit(feedback)

        elif not mult:
            start = time.time()
            name = RL_2D_deconvolve(itera, sigma, pixel, filename, psf, output, mult, label, out_name)
            end = time.time()

            time_taken = str(end - start)
            feedback = fDS(time_taken, itera, name)
            self.signal_1.emit(feedback)

    def decon_2D_color(self, psf_gen, mult, itera, sigma, pixel, filename, output, label, out_name):
        psf = self.psfGen2D(sigma, pixel, output, psf_gen)
        if mult:
            iter = []
            min = 1
            while min <= itera:
                iter.append(min)
                min += 1
            for x in iter:
                start = time.time()
                name = RL_Color_Deconvolution(x, sigma, pixel, filename, psf, output, mult, label, out_name)
                end = time.time()

                time_taken = str(end - start)
                feedback = fDS(time_taken, x, name)
                self.signal_1.emit(feedback)

        elif not mult:
            start = time.time()
            name = RL_Color_Deconvolution(itera, sigma, pixel, filename, psf, output, mult, label, out_name)
            end = time.time()

            time_taken = str(end - start)
            feedback = fDS(time_taken, itera, name)
            self.signal_1.emit(feedback)
