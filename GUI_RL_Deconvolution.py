import threading

import function_handler
from Run_Deconvolution import *
from Generate_PSF import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QFileDialog, \
    QSpinBox, QCheckBox, QGroupBox, QWidget, QTabWidget, QVBoxLayout, QGridLayout, QToolButton, QProgressBar, \
    QPlainTextEdit, QDoubleSpinBox

from feedback_DS import feedback_DS as fDS


class MainWindow(QMainWindow):
    def set_filename(self, x):
        self._filename = x

    def get_filename(self):
        return self._filename

    def set_output_path(self, x):
        self._output_path = x

    def get_output_path(self):
        return self._output_path

    def set_index_position(self, x):
        self._index_position = x

    def get_index_position(self):
        return self._index_position

    def set_out_file_name(self, x):
        self._out_file_name = x

    def get_out_file_name(self):
        return self._out_file_name

    def __init__(self):
        super().__init__()
        self._out_file_name = None
        self._index_position = 0
        self.set_output = None
        self._output_path = None
        self._filename = None
        self.title = "Richardson Lucy Deconvolution"
        self.setWindowIcon(QIcon("Assets/project_icon_2.png"))
        self.left = 0
        self.top = 0
        self.width = 1400
        self.height = 1000
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        app.setStyleSheet('QLabel{font-size: 16pt;}'
                          'QComboBox{font-size: 12pt;}'
                          'QPushButton{font-size: 12pt;}'
                          'QSpinBox{font-size: 12pt;}'
                          'QDoubleSpinBox{font-size: 12pt;}'
                          'QCheckBox{font-size: 12pt;}'
                          'QGroupBox{border: 2px solid gray;border-radius: 5px;background: rgb(211, 218, 235);}'
                          'Selection-color: grey;')

        self.tabs_window = CreateWindow(self)
        self.setCentralWidget(self.tabs_window)

        self.show()


class CreateWindow(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.fun = None
        self.thread = None
        self._Progress = 0
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(1200, 900)

        self.tabs.addTab(self.tab1, "Input")
        self.tabs.addTab(self.tab2, "Output")

        self.tab1.layout = QGridLayout(self)

        # region tab1
        top_group = QGroupBox(self)

        decon_type = QLabel('Deconvolution type:', self)

        self.type_box = QComboBox(self)
        self.type_box.addItem("1D Deconvolution")
        self.type_box.addItem("2D Deconvolution (Grey)")
        self.type_box.addItem("2D Deconvolution (Color)")
        self.type_box.setFixedSize(300, 50)

        file_sel = QLabel('Select File:', self)

        search = QPushButton('Search', self)
        search.clicked.connect(self.input_file)
        search.setFixedSize(300, 50)

        right_top_group = QGroupBox(self)

        logo_img = QLabel(self)
        self.logo_map = QPixmap('./Assets/logo.png')
        self.logo_resize = self.logo_map.scaled(425, 200)
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

        self.sigma_sel = QDoubleSpinBox(self)
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

        self.mult = QCheckBox('Generate Image for each Iteration', self)
        self.mult.setChecked(True)

        self.psf_gen = QCheckBox('Generate PSF Image', self)
        self.psf_gen.setChecked(True)

        self.label = QCheckBox('Label Image with iteration value', self)
        self.label.setChecked(True)

        self.run = QPushButton('Run Deconvolution', self)
        self.run.setFixedSize(300, 100)
        self.run.clicked.connect(self.start_deconvolution)

        bottom_text = QLabel("Acadia Physics 2023", self)

        bottom_text.setStyleSheet('font-size: 8pt;')

        space = QLabel()
        self.tab1.layout.addWidget(self.image_label, 6, 4, 60, 80, alignment=Qt.AlignmentFlag.AlignLeft)
        self.tab1.layout.addWidget(preview, 10, 4, 4, 24)

        self.tab1.layout.addWidget(space, 0, 0, 72, 0)  # left side
        self.tab1.layout.addWidget(space, 0, 0, 0, 96)  # top

        self.tab1.layout.addWidget(top_group, 1, 1, 8, 76)

        self.tab1.layout.addWidget(decon_type, 1, 4, 2, 24)
        self.tab1.layout.addWidget(self.type_box, 1, 36, 2, 24)

        self.tab1.layout.addWidget(file_sel, 4, 4, 2, 32)
        self.tab1.layout.addWidget(search, 4, 36, 2, 24)

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
        self.tab1.layout.addWidget(self.mult, 48, 78, 4, 18)
        self.tab1.layout.addWidget(self.psf_gen, 52, 78, 4, 18)
        self.tab1.layout.addWidget(self.label, 56, 78, 4, 18)

        self.tab1.layout.addWidget(self.run, 56, 16, 8, 24)
        self.tab1.layout.addWidget(bottom_text, 61, 90, 2, 6)
        # endregion

        # region tab2
        self.tab2.layout = QGridLayout(self)
        self.filelist = []
        sys.stdout = sys.__stdout__

        logo_img_out = QLabel(self)
        logo_map_out = QPixmap('./Assets/logo.png')
        logo_resize_out = logo_map_out.scaled(450, 200)
        logo_img_out.setPixmap(logo_resize_out)
        logo_img_out.adjustSize()

        logo_out = QLabel('Image Deconvolution', self)
        logo_out.setFixedSize(450, 75)
        logo_out.setStyleSheet('color: white;font-size: 20pt;')

        iter_num = QLabel("RL Interation")
        self.iter_value = QLabel(" ", self)

        left_arrow = QToolButton(self)
        left_arrow.setArrowType(Qt.LeftArrow)
        left_arrow.setFixedSize(100, 100)
        left_arrow.clicked.connect(self.img_left)

        right_arrow = QToolButton(self)
        right_arrow.setArrowType(Qt.RightArrow)
        right_arrow.setFixedSize(100, 100)
        right_arrow.clicked.connect(self.img_right)

        self.pbar = QProgressBar(self)

        self.out_img = QLabel()

        self.feed = QPlainTextEdit()
        self.feed.setFixedSize(600, 300)
        self.feed.setReadOnly(True)
        self.feed.setStyleSheet("font-size: 12pt")

        space2 = QLabel()
        self.tab2.layout.addWidget(space2, 0, 0, 72, 1)  # left side
        self.tab2.layout.addWidget(space2, 0, 0, 1, 96)  # top
        self.tab2.layout.addWidget(logo_img_out, 1, 80, 8, 16)
        self.tab2.layout.addWidget(logo_out, 5, 81, 4, 16)
        self.tab2.layout.addWidget(iter_num, 12, 85, 4, 16)
        self.tab2.layout.addWidget(self.iter_value, 14, 87, 4, 16)
        self.tab2.layout.addWidget(left_arrow, 15, 80, 4, 16)
        self.tab2.layout.addWidget(right_arrow, 15, 92, 4, 16)
        self.tab2.layout.addWidget(self.pbar, 42, 5, 6, 64)
        self.tab2.layout.addWidget(self.out_img, 1, 1, 32, 32)
        self.tab2.layout.addWidget(self.feed, 25, 72, 32, 32)

        # endregion

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)
        self.tab1.setLayout(self.tab1.layout)
        self.tab2.setLayout(self.tab2.layout)

        self.worker = function_handler.funcThread(self)
        self.worker.signal_1.connect(self.update)

    def update(self, fDS):
        print("updating")

        self.feed.appendPlainText("Running {} RL".format(fDS.getNumIterations()))
        self.pbar.setValue(int(fDS.getNumIterations()))
        self.iter_value.setText(str(fDS.getNumIterations()))

        self.create_img(fDS.getName())
        self.feed.appendPlainText("Iteration with RL{} completed\nRun took {} seconds".format(fDS.getNumIterations(), fDS.getTime()))
        print("complete")


    def start_deconvolution(self):
        plt.clf()
        self.tabs.setCurrentIndex(1)
        mult_state = self.mult.isChecked()
        label_state = self.label.isChecked()
        gen_psf = self.psf_gen.isChecked()

        if window.get_filename():
            if window.get_output_path() is None:
                window.set_output_path("out")
            run_type = self.type_box.currentText()

            self.feed.appendPlainText("{}".format(run_type))
            sigma2 = self.sigma_sel.value()
            itera2 = self.itera_sel.value()
            pixels2 = self.pixels_sel.value()
            i = 0
            self.filelist = []
            self.pbar.setRange(0, itera2)
            while itera2 < i:
                filename = window.get_output_path()
                name = os.path.basename(filename) + " " + "pixel" + str(pixels2) + "RL" + str(itera2) + "sig" + str(
                    sigma2) + ".png"
                self.filelist.append(name)
                i += 1

            if run_type == "1D Deconvolution":
                self.feed.appendPlainText("Running {} RL".format(itera2))
                self.worker.decon_1D(gen_psf, mult_state, itera2, sigma2, pixels2, window.get_filename(),
                                     window.get_output_path(), label_state, window.get_out_file_name())

            elif run_type == "2D Deconvolution (Grey)":
                self.feed.appendPlainText("Running {} RL".format(itera2))
                self.worker.decon_2D_gray(gen_psf, mult_state, itera2, sigma2, pixels2, window.get_filename(),
                                          window.get_output_path(), label_state, window.get_out_file_name())

            elif run_type == "2D Deconvolution (Color)":
                self.feed.appendPlainText("Running {} RL".format(itera2))
                self.worker.decon_2D_color(gen_psf, mult_state, itera2, sigma2, pixels2, window.get_filename(),
                                           window.get_output_path(), label_state, window.get_out_file_name())

        else:
            print("No file Selected")
        plt.clf()

    def input_file(self):
        self.image_label.clear()
        run_type = self.type_box.currentText()
        if run_type == "1D Deconvolution":
            tmp = "./tmp.png"
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
                plt.savefig("./tmp.png")
                pixmap = QPixmap("./tmp.png")
                pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap_resized)
                self.image_label.adjustSize()
                window.set_filename(file_dialog[0])
            plt.clf()

        elif run_type == "2D Deconvolution (Grey)" or run_type == "2D Deconvolution (Color)":
            file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                        './Images_Input', "Image files (*.jpg *.tif *.png)")
            image_path = file_dialog[0]
            res = os.path.isfile(image_path)
            if res:
                window.set_filename(file_dialog[0])
                pixmap = QPixmap(image_path)
                pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
                self.image_label.setPixmap(pixmap_resized)
                self.image_label.adjustSize()
            plt.clf()

    def img_left(self):
        itera2 = self.itera_sel.value()
        x = window.get_index_position()
        if itera2 > 0:
            if x > 0:
                x -= 1
                window.set_index_position(x)
                self.iter_value.setText("{}".format(x))
                self.create_img(window.get_out_file_name(), window.get_index_position())

    def img_right(self):
        itera2 = self.itera_sel.value()
        x = window.get_index_position()
        if itera2 > 0:
            if x < itera2:
                x += 1
                window.set_index_position(x)
                self.iter_value.setText("{}".format(x))
                self.create_img(window.get_out_file_name(), window.get_index_position())

    def create_img(self, file):
        name = "out/" + file
        pixmap = QPixmap(name)
        pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
        self.out_img.setPixmap(pixmap_resized)
        self.out_img.adjustSize()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
