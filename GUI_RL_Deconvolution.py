import sys
import typing
from Run_Deconvolution import *
from Generate_PSF import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QFileDialog, \
    QSpinBox, QCheckBox, QGroupBox, QWidget, QTabWidget, QVBoxLayout


class MainWindow(QMainWindow):
    input_file = None
    def set_sigma(self, x):
        self._sigma = x
    def get_sigma(self):
        return self._sigma
    def get_itera(self):
        return self._itera
    def set_itera(self, x):
        self._itera = x
    def get_pixels(self):
        return self._pixels
    def set_pixels(self, x):
        self._pixels = x
    def set_filename(self, x):
        self._filename = x
    def get_filename(self):
        return self._filename
    def set_output_path(self, x):
        self._output_path = x
    def get_output_path(self):
        return self._output_path
    def get_mult_img(self):
        return self._mult_img
    def set_mult_img(self, x):
        self._mult_img = x
    def get_label_state(self):
        return self._label_state
    def set_label_state(self, x):
        self._label_state = x
    def set_psf_gen(self, x):
        self._psf_gen = x
    def get_psf_gen(self):
        return self._psf_gen
    def __init__(self):
        super().__init__()
        self.input_file = None
        self._input_file = None
        self._label_state = None
        self.out = None
        self._psf_gen = None
        self._label = None
        self._mult = None
        self._mult_img = None
        self.plot_graph = None
        self.type_box = None
        self._output_path = None
        self._filename = None
        self._sigma = None
        self._pixels = None
        self._itera = None
        self.sigma_sel = None
        self.itera_sel = None
        self.pixels_sel = None
        self.image_label = None
        self.layout = QVBoxLayout(self)
        self.title = "Richardson Lucy Deconvolution"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left = 50
        self.top = 50
        self.setFixedSize(1200, 950)
        app.setStyleSheet('QLabel{font-size: 16pt;}'
                          'QComboBox{font-size: 12pt;}'
                          'QPushButton{font-size: 12pt;}'
                          'QSpinBox{font-size: 12pt;}'
                          'QCheckBox{font-size: 12pt;}'
                          'QGroupBox{border: 2px solid gray;border-radius: 5px;background: rgb(211, 218, 235);}'
                          'Selection-color: grey;')
        self.tabs = QTabWidget(self)
        tab1 = QWidget(self)
        tab2 = QWidget(self)
        self.tabs.resize(1200, 950)
        self.layout.addWidget(self.tabs)
        self.tabs.addTab(tab1, "Input")
        self.tabs.addTab(tab2, "Output")

        createTab1.create_tab1(tab1)
        createTab2.create_tab2(tab2)

        self.show()


class createTab1(QMainWindow):

    def create_tab1(self):
        top_group = QGroupBox(self)
        top_group.move(25, 60)
        top_group.setFixedSize(700, 165)

        decon_type = QLabel('Deconvolution type:', self)
        decon_type.setFixedSize(300, 50)
        decon_type.move(50, 75)

        type_box = QComboBox(self)
        type_box.addItem("1D Deconvolution")
        type_box.addItem("2D Deconvolution")
        type_box.setFixedSize(300, 50)
        type_box.move(400, 80)

        file_sel = QLabel('Select File:', self)
        file_sel.setFixedSize(300, 50)
        file_sel.move(50, 150)

        search = QPushButton('Search', self)
        search.setFixedSize(300, 50)
        search.move(400, 150)
        search.clicked.connect(lambda: self.input_file)

        right_top_group = QGroupBox(self)
        right_top_group.move(725, 300)
        right_top_group.setFixedSize(450, 250)

        logo_img = QLabel(self)
        logo_img.move(750, 60)
        logo_map = QPixmap('./Assets/logo.png')
        logo_resize = logo_map.scaled(425, 400, QtCore.Qt.KeepAspectRatio)
        logo_img.setPixmap(logo_resize)
        logo_img.adjustSize()

        logo = QLabel('Image Deconvolution', self)
        logo.move(775, 150)
        logo.setFixedSize(400, 100)
        logo.setStyleSheet('color: white;font-size: 20pt;')

        preview = QLabel('Image Preview:', self)
        preview.move(50, 250)
        preview.setFixedSize(300, 50)
        image_label = QLabel(self)
        image_label.move(50, 300)

        decon_label = QLabel('Deconvolution settings:', self)
        decon_label.move(750, 250)
        decon_label.setFixedSize(350, 50)

        sigma = QLabel('Sigma:', self)
        sigma.move(750, 325)
        sigma.setFixedSize(150, 50)

        pixels = QLabel('Pixels:', self)
        pixels.move(750, 400)
        pixels.setFixedSize(150, 50)

        itera = QLabel('Iterations:', self)
        itera.move(750, 475)
        itera.setFixedSize(150, 50)

        sigma_sel = QSpinBox(self)
        sigma_sel.move(1000, 325)
        sigma_sel.setFixedSize(150, 50)
        sigma_sel.setMaximum(9999)
        sigma_sel.setValue(10)

        pixels_sel = QSpinBox(self)
        pixels_sel.move(1000, 400)
        pixels_sel.setFixedSize(150, 50)
        pixels_sel.setMaximum(9999)
        pixels_sel.setValue(100)

        itera_sel = QSpinBox(self)
        itera_sel.move(1000, 475)
        itera_sel.setFixedSize(150, 50)
        itera_sel.setMaximum(9999)
        itera_sel.setValue(50)

        right_bottom_group = QGroupBox(self)
        right_bottom_group.move(725, 625)
        right_bottom_group.setFixedSize(450, 250)

        output_settings = QLabel("Output Settings:", self)
        output_settings.move(750, 575)
        output_settings.setFixedSize(400, 50)

        output_dir = QPushButton("Output Directory", self)
        output_dir.move(750, 650)
        output_dir.setFixedSize(400, 50)
        output_dir.clicked.connect(lambda: self.set_output)

        mult = QCheckBox('Generate Image for each Iteration', self)
        mult.move(750, 700)
        mult.setFixedSize(400, 50)
        mult.setChecked(True)

        psf_gen = QCheckBox('Generate PSF Image', self)
        psf_gen.move(750, 750)
        psf_gen.setFixedSize(400, 50)
        psf_gen.setChecked(True)

        label = QCheckBox('Label Image with iteration value', self)
        label.move(750, 800)
        label.setFixedSize(400, 50)
        label.setChecked(True)

        run = QPushButton('Run Deconvolution', self)
        run.setFixedSize(300, 100)
        run.move(200, 800)
        run.clicked.connect(lambda: self.start_deconvolution)

        bottom_text = QLabel("Acadia Physics 2023", self)
        bottom_text.setFixedSize(200, 25)
        bottom_text.move(1050, 875)
        bottom_text.setStyleSheet('font-size: 8pt;')

    def set_output(self):
        output_path = QFileDialog().getExistingDirectory(self, None, "Select Folder")
        window.set_output_path(output_path)

    def start_deconvolution(self):
        mult_state = self.mult.isChecked()
        self.set_mult_img(mult_state)
        label_state = self.label.isChecked()
        self.set_label_state(label_state)
        gen_psf = self.psf_gen.isChecked()
        self.set_psf_gen(gen_psf)
        if window.get_filename():
            if window.get_output_path() is None:
                window.set_output_path(".")
            run_type = self.type_box.currentText()
            print(run_type)
            sigma2 = self.sigma_sel.value()
            itera2 = self.itera_sel.value()
            pixels2 = self.pixels_sel.value()
            window.set_sigma(sigma2)
            window.set_itera(itera2)
            window.set_pixels(pixels2)
            if run_type == "1D Deconvolution":
                psf = generate_1D_psf(window.get_sigma(), window.get_pixels(),
                                      window.get_output_path(), window.get_psf_gen())
                RL_1D_Deconvolve(window.get_itera(), window.get_sigma(), window.get_pixels(),
                                 window.get_filename(), psf, window.get_output_path(),
                                 window.get_mult_img(), window.get_label_state())

            elif run_type == "2D Deconvolution":
                psf = generate_2D_psf(window.get_sigma(), window.get_pixels(),
                                      window.get_output_path(), window.get_psf_gen())
                RL_2D_deconvolve(window.get_itera(), window.get_sigma(), window.get_pixels(),
                                 window.get_filename(), psf, window.get_output_path(),
                                 window.get_mult_img(), window.get_label_state())

        else:
            print("No file Selected")

    def input_file(self):
        run_type = self.type_box.currentText()
        if run_type == "1D Deconvolution":
            tmp = "./tmp.tif"
            if os.path.isfile(tmp):
                os.remove(tmp)
            file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                        './Images_Input', "Text Files (*.txt)")
            image_path = file_dialog[0]
            f = open('{}'.format(image_path), 'r')
            x_axis = []
            spectra = []
            for line in f:
                line = line.strip().split('\t')
                x_axis.append((line[0]))
                spectra.append(line[1])
            spectra_plt = np.array(spectra, dtype=np.float32)
            plt.plot(spectra_plt)
            plt.savefig("./tmp.tif")
            pixmap = QPixmap("./tmp.tif")
            pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap_resized)
            self.image_label.adjustSize()
            window.set_filename(image_path)
            plt.cla()

        elif run_type == "2D Deconvolution":
            file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                        './Images_Input', "Image files (*.jpg *.tif)")
            image_path = file_dialog[0]
            window.set_filename(image_path)
            pixmap = QPixmap(image_path)
            pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap_resized)
            self.image_label.adjustSize()



class createTab2(QMainWindow):
    def create_tab2(self):
        logo_img_out = QLabel(self)
        logo_img_out.move(850, 10)
        logo_map_out = QPixmap('./Assets/logo.png')
        logo_resize_out = logo_map_out.scaled(300, 200, QtCore.Qt.KeepAspectRatio)
        logo_img_out.setPixmap(logo_resize_out)
        logo_img_out.adjustSize()

        logo_out = QLabel('Image Deconvolution', self)
        logo_out.move(850, 75)
        logo_out.setFixedSize(450, 75)
        logo_out.setStyleSheet('color: white;font-size: 16pt;')


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
