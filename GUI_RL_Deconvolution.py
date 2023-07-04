import sys
from Run_Deconvolution import *
from Generate_PSF import *
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QComboBox, QFileDialog, \
    QSpinBox, QCheckBox, QGroupBox, QWidget, QTabWidget, QVBoxLayout


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
        self.left = 50
        self.top = 50
        self.setFixedSize(1200, 900)
        app.setStyleSheet('QLabel{font-size: 16pt;}'
                          'QComboBox{font-size: 12pt;}'
                          'QPushButton{font-size: 12pt;}'
                          'QSpinBox{font-size: 12pt;}'
                          'QCheckBox{font-size: 12pt;}'
                          'QGroupBox{border: 2px solid gray;border-radius: 5px;background: rgb(211, 218, 235);}'
                          'Selection-color: grey;')
        self.initUI()
        self.init_out()

    def initUI(self):
        self.tabs = QTabWidget(self)
        self.tab1 = QWidget(self)
        self.tab2 = QWidget(self)
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Input")
        self.tabs.addTab(self.tab2, "Output")

        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon("./Assets/projecticon2.png"))

        self.tab1.layout = QVBoxLayout(self)
        top_group = QGroupBox(self)
        top_group.move(25, 60)
        top_group.setFixedSize(700, 165)

        Decon_type = QLabel('Deconvolution type:', self)
        Decon_type.setFixedSize(300, 50)
        Decon_type.move(50, 75)

        self.type_box = QComboBox(self)
        self.type_box.addItem("1D Deconvolution")
        self.type_box.addItem("2D Deconvolution")
        self.type_box.setFixedSize(300, 50)
        self.type_box.move(400, 80)

        file_sel = QLabel('Select File:', self)
        file_sel.setFixedSize(300, 50)
        file_sel.move(50, 150)

        search = QPushButton('Search', self)
        search.setFixedSize(300, 50)
        search.move(400, 150)
        search.clicked.connect(self.get_file)

        righttop_group = QGroupBox(self)
        righttop_group.move(725, 300)
        righttop_group.setFixedSize(450, 250)

        logo_img = QLabel(self)
        logo_img.move(750, 60)
        logo_map = QPixmap('./Assets/logo.png')
        logo_resize = logo_map.scaled(425, 400, QtCore.Qt.KeepAspectRatio)
        logo_img.setPixmap(logo_resize)
        logo_img.adjustSize()

        Logo = QLabel('Image Deconvolution', self)
        Logo.move(775, 150)
        Logo.setFixedSize(400, 100)
        Logo.setStyleSheet('color: white;font-size: 20pt;')

        preview = QLabel('Image Preview:', self)
        preview.move(50, 250)
        preview.setFixedSize(300, 50)
        self.image_label = QLabel(self)
        self.image_label.move(50, 300)

        Decon_label = QLabel('Deconvolution settings:', self)
        Decon_label.move(750, 250)
        Decon_label.setFixedSize(350, 50)

        sigma = QLabel('Sigma:', self)
        sigma.move(750, 325)
        sigma.setFixedSize(150, 50)

        pixels = QLabel('Pixels:', self)
        pixels.move(750, 400)
        pixels.setFixedSize(150, 50)

        itera = QLabel('Iterations:', self)
        itera.move(750, 475)
        itera.setFixedSize(150, 50)

        self.sigma_sel = QSpinBox(self)
        self.sigma_sel.move(1000, 325)
        self.sigma_sel.setFixedSize(150, 50)
        self.sigma_sel.setMaximum(9999)
        self.sigma_sel.setValue(10)

        self.pixels_sel = QSpinBox(self)
        self.pixels_sel.move(1000, 400)
        self.pixels_sel.setFixedSize(150, 50)
        self.pixels_sel.setMaximum(9999)
        self.pixels_sel.setValue(100)

        self.itera_sel = QSpinBox(self)
        self.itera_sel.move(1000, 475)
        self.itera_sel.setFixedSize(150, 50)
        self.itera_sel.setMaximum(9999)
        self.itera_sel.setValue(50)

        rightbottom_group = QGroupBox(self)
        rightbottom_group.move(725, 625)
        rightbottom_group.setFixedSize(450, 250)

        Output_settings = QLabel("Output Settings:", self)
        Output_settings.move(750, 575)
        Output_settings.setFixedSize(400, 50)

        output_dir = QPushButton("Output Directory", self)
        output_dir.move(750, 650)
        output_dir.setFixedSize(400, 50)
        output_dir.clicked.connect(self.set_output)

        self.mult = QCheckBox('Generate Image for each Iteration', self)
        self.mult.move(750, 700)
        self.mult.setFixedSize(400, 50)
        self.mult.setChecked(True)

        self.psf_gen = QCheckBox('Generate PSF Image', self)
        self.psf_gen.move(750, 750)
        self.psf_gen.setFixedSize(400, 50)
        self.psf_gen.setChecked(True)

        self.label = QCheckBox('Label Image with iteration value', self)
        self.label.move(750, 800)
        self.label.setFixedSize(400, 50)
        self.label.setChecked(True)

        run = QPushButton('Run Deconvolution', self)
        run.setFixedSize(300, 100)
        run.move(200, 800)
        run.clicked.connect(self.start_deconvolution)

        bottom_text = QLabel("Acadia Physics 2023", self)
        bottom_text.setFixedSize(200, 25)
        bottom_text.move(1050, 875)
        bottom_text.setStyleSheet('font-size: 8pt;')

        self.tab1.layout.addWidget(bottom_text)
        self.tab1.layout.addWidget(file_sel)
        self.tab1.layout.addWidget(itera)
        self.tab1.layout.addWidget(logo_img)
        self.tab1.layout.addWidget(output_dir)
        self.tab1.layout.addWidget(preview)
        self.tab1.layout.addWidget(run)
        self.tab1.layout.addWidget(righttop_group)
        self.tab1.layout.addWidget(rightbottom_group)
        self.tab1.layout.addWidget(sigma)
        self.tab1.layout.addWidget(top_group)





        self.show()

    def get_file(self):
        run_type = self.type_box.currentText()
        if run_type == "1D Deconvolution":
            tmp = "./tmp.tif"
            if os.path.isfile(tmp):
                os.remove(tmp)
            file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                        './Images_Input', "Text Files (*.txt)")
            imagePath = file_dialog[0]
            f = open('{}'.format(imagePath), 'r')
            xaxis = []
            spectra = []
            for line in f:
                line = line.strip().split('\t')
                xaxis.append((line[0]))
                spectra.append(line[1])
            spectraplt = np.array(spectra, dtype=np.float32)
            plt.plot(spectraplt)
            plt.savefig("./tmp.tif")
            pixmap = QPixmap("./tmp.tif")
            pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap_resized)
            self.image_label.adjustSize()
            window.set_filename(imagePath)
            plt.cla()

        elif run_type == "2D Deconvolution":
            file_dialog = QFileDialog().getOpenFileName(self, 'Open file',
                                                        './Images_Input', "Image files (*.jpg *.tif)")
            imagePath = file_dialog[0]
            window.set_filename(imagePath)
            pixmap = QPixmap(imagePath)
            pixmap_resized = pixmap.scaled(650, 650, QtCore.Qt.KeepAspectRatio)
            self.image_label.setPixmap(pixmap_resized)
            self.image_label.adjustSize()

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

    def init_out(self):
        self.title = "Richardson Lucy Deconvolution output"
        self.setWindowIcon(QIcon("./Assets/projecticon2.png"))

        logo_img_out = QLabel(self)
        logo_img_out.move(800, 10)
        logo_map_out = QPixmap('./Assets/logo.png')
        logo_resize_out = logo_map_out.scaled(300, 200, QtCore.Qt.KeepAspectRatio)
        logo_img_out.setPixmap(logo_resize_out)
        logo_img_out.adjustSize()

        Logo = QLabel('Image Deconvolution', self)
        Logo.move(800, 100)
        Logo.setFixedSize(450, 75)
        Logo.setStyleSheet('color: white;font-size: 16pt;')


app = QApplication(sys.argv)
window = MainWindow()
app.exec_()
