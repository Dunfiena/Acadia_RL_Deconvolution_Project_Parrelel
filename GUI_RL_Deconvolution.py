import sys
from Run_Deconvolution import *
from Generate_PSF import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QFileDialog, \
    QSpinBox, QCheckBox, QGroupBox, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QToolButton


class MainWindow(QMainWindow):
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
        self.img_arr = []
        self.set_output = None
        self._psf_gen = None
        self._label_state = None
        self._mult_img = None
        self._output_path = None
        self._filename = None
        self._pixels = None
        self._itera = None
        self._sigma = None
        self.title = "Richardson Lucy Deconvolution"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left = 0
        self.top = 0
        self.width = 1200
        self.height = 900
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        app.setStyleSheet('QLabel{font-size: 16pt;}'
                          'QComboBox{font-size: 12pt;}'
                          'QPushButton{font-size: 12pt;}'
                          'QSpinBox{font-size: 12pt;}'
                          'QCheckBox{font-size: 12pt;}'
                          'QGroupBox{border: 2px solid gray;border-radius: 5px;background: rgb(211, 218, 235);}'
                          'Selection-color: grey;')
        self.tabs_window = create_window(self)
        self.setCentralWidget(self.tabs_window)

        self.show()


class create_window(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(1200, 900)

        self.tabs.addTab(self.tab1, "Input")
        self.tabs.addTab(self.tab2, "Output")
        self.tab1.layout = QGridLayout(self)

        top_group = QGroupBox(self)

        decon_type = QLabel('Deconvolution type:', self)

        self.type_box = QComboBox(self)
        self.type_box.addItem("1D Deconvolution")
        self.type_box.addItem("2D Deconvolution")
        self.type_box.setFixedSize(300, 50)

        file_sel = QLabel('Select File:', self)

        search = QPushButton('Search', self)
        search.clicked.connect(self.input_file)
        search.setFixedSize(300, 50)

        right_top_group = QGroupBox(self)

        logo_img = QLabel(self)
        self.logo_map = QPixmap('./Assets/logo.png')
        self.logo_resize = self.logo_map.scaled(425, 400, QtCore.Qt.KeepAspectRatio)
        logo_img.setPixmap(self.logo_resize)
        logo_img.adjustSize()

        logo = QLabel('Image Deconvolution', self)
        logo.setStyleSheet('color: white;font-size: 20pt;')

        preview = QLabel('Image Preview:', self)

        self.image_label = QLabel(self)

        decon_label = QLabel('Deconvolution settings:', self)

        sigma = QLabel('Sigma:', self)
        pixels = QLabel('Pixels:', self)
        itera = QLabel('Iterations:', self)

        self.sigma_sel = QSpinBox(self)
        self.sigma_sel.setMaximum(9999)
        self.sigma_sel.setValue(10)
        self.sigma_sel.setFixedSize(150, 50)

        self.pixels_sel = QSpinBox(self)
        self.pixels_sel.setMaximum(9999)
        self.pixels_sel.setValue(100)
        self.pixels_sel.setFixedSize(150, 50)

        self.itera_sel = QSpinBox(self)
        self.itera_sel.setMaximum(9999)
        self.itera_sel.setValue(50)
        self.itera_sel.setFixedSize(150, 50)

        right_bottom_group = QGroupBox(self)
        output_settings = QLabel("Output Settings:", self)

        output_dir = QPushButton("Output Directory", self)
        output_dir.clicked.connect(self.set_output)

        self.mult = QCheckBox('Generate Image for each Iteration', self)
        self.mult.setChecked(True)

        self.psf_gen = QCheckBox('Generate PSF Image', self)
        self.psf_gen.setChecked(True)

        self.label = QCheckBox('Label Image with iteration value', self)
        self.label.setChecked(True)

        run = QPushButton('Run Deconvolution', self)
        run.setFixedSize(300, 100)
        run.clicked.connect(self.start_deconvolution)

        bottom_text = QLabel("Acadia Physics 2023", self)

        bottom_text.setStyleSheet('font-size: 8pt;')

        space = QLabel()
        self.tab1.layout.addWidget(self.image_label, 6, 4, 60, 80, alignment=Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(preview, 10, 4, 4, 24)

        self.tab1.layout.addWidget(space, 0, 0, 72, 1)  # left side
        self.tab1.layout.addWidget(space, 0, 0, 1, 96)  # top

        self.tab1.layout.addWidget(top_group, 1, 1, 8, 76)

        self.tab1.layout.addWidget(decon_type, 2, 4, 2, 24)
        self.tab1.layout.addWidget(self.type_box, 2, 36, 2, 24)

        self.tab1.layout.addWidget(file_sel, 5, 4, 2, 32)
        self.tab1.layout.addWidget(search, 5, 36, 2, 24)

        self.tab1.layout.addWidget(logo_img, 1, 80, 8, 16)
        self.tab1.layout.addWidget(logo, 5, 81, 4, 16)

        self.tab1.layout.addWidget(right_top_group, 14, 76, 20, 20)
        self.tab1.layout.addWidget(decon_label, 10, 76, 4, 20)
        self.tab1.layout.addWidget(sigma, 16, 78, 4, 16)
        self.tab1.layout.addWidget(pixels, 22, 78, 4, 16)
        self.tab1.layout.addWidget(itera, 28, 78, 4, 16)
        self.tab1.layout.addWidget(self.sigma_sel, 16, 88, 4, 6)
        self.tab1.layout.addWidget(self.pixels_sel, 22, 88, 4, 6)
        self.tab1.layout.addWidget(self.itera_sel, 28, 88, 4, 6)

        self.tab1.layout.addWidget(right_bottom_group, 40, 76, 24, 20)
        self.tab1.layout.addWidget(output_settings, 36, 76, 4, 20)
        self.tab1.layout.addWidget(output_dir, 42, 78, 4, 17)
        self.tab1.layout.addWidget(self.mult, 48, 78, 4, 18)
        self.tab1.layout.addWidget(self.psf_gen, 52, 78, 4, 18)
        self.tab1.layout.addWidget(self.label, 56, 78, 4, 18)

        self.tab1.layout.addWidget(run, 62, 16, 8, 24)
        self.tab1.layout.addWidget(bottom_text, 66, 90, 2, 6)

        # Output Tab QWidgets
        self.tab2.layout = QGridLayout(self)

        logo_img_out = QLabel(self)
        logo_map_out = QPixmap('./Assets/logo.png')
        logo_resize_out = logo_map_out.scaled(450, 400, QtCore.Qt.KeepAspectRatio)
        logo_img_out.setPixmap(logo_resize_out)
        logo_img_out.adjustSize()

        logo_out = QLabel('Image Deconvolution', self)
        logo_out.setFixedSize(450, 75)
        logo_out.setStyleSheet('color: white;font-size: 20pt;')

        iter_num = QLabel("RL Interation")

        left_arrow = QToolButton(self)
        left_arrow.setArrowType(Qt.LeftArrow)
        left_arrow.setFixedSize(100, 100)
        left_arrow.clicked.connect(self.Img_left)

        right_arrow = QToolButton(self)
        right_arrow.setArrowType(Qt.RightArrow)
        right_arrow.setFixedSize(100, 100)
        right_arrow.clicked.connect(self.Img_right)

        out_img = QLabel()

        self.tab2.layout.addWidget(space, 0, 0, 72, 1)  # left side
        self.tab2.layout.addWidget(space, 0, 0, 1, 96)  # top
        self.tab2.layout.addWidget(logo_img_out, 1, 80, 8, 16)
        self.tab2.layout.addWidget(logo_out, 5, 81, 4, 16)
        self.tab2.layout.addWidget(iter_num, 12, 85, 4, 16)
        self.tab2.layout.addWidget(left_arrow, 15, 80, 4, 16)
        self.tab2.layout.addWidget(right_arrow, 15, 92, 4, 16)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)

    def set_output(self):
        output_path = QFileDialog().getExistingDirectory(self, None, "Select Folder")
        window.set_output_path(output_path)

    def start_deconvolution(self):
        mult_state = self.mult.isChecked()
        window.set_mult_img(mult_state)
        label_state = self.label.isChecked()
        window.set_label_state(label_state)
        gen_psf = self.psf_gen.isChecked()
        window.set_psf_gen(gen_psf)

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
                print(window.img_arr)
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
            res = os.path.isfile(image_path)
            if res:
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
            res = os.path.isfile(image_path)
            if res:
                print("ab")
                window.set_filename(image_path)
                pixmap = QPixmap(image_path)
                pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap_resized)
                self.image_label.adjustSize()

    def Img_left(self):
        img_num = 0

    def Img_right(self):
        img_num = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
