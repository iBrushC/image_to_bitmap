# All code written by Andrew Michael Combs

# Imports
import numpy as np

from os.path import expanduser
import sys

from numpy.lib.npyio import save

from filehandler import *
from ditherer import *
from imagehandler import *

import PyQt5
from PyQt5.QtCore import QRect, Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (
    QApplication,
    QBoxLayout,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QLineEdit, 
    QMainWindow,
    QSizePolicy,
    QSpacerItem,

    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QLayout,

    QPushButton
)
from PyQt5 import QtGui
from PyQt5.QtGui import (
    QDropEvent,
    QIcon,
    QImage,
    QPainter,
    QPixmap,
    QResizeEvent
) 

# Image view box
class ImageView(QWidget):
    #Init
    def __init__(self, fp):
        super().__init__()
        
        self.fp = fp
        self.pixmap = QPixmap(self.fp)

        if self.fp == "":
            return

        self.px, self.py = self.pixmap.width(), self.pixmap.height()

        self.set_constraints()

    # Set new image
    def set_pixmap(self, fp):

        self.fp = fp
        self.pixmap = QPixmap(self.fp)

        if self.fp == "":
            return
        
        grayscale = self.pixmap.copy().toImage().convertToFormat(QImage.Format_Grayscale8)
        self.pixmap = QPixmap.fromImage(grayscale)
        self.px, self.py = self.pixmap.width(), self.pixmap.height()

        self.set_constraints()

        self.update()

    # Set minimum and maximum size constraints
    def set_constraints(self):
        self.setMinimumWidth(int(self.px/10))
        self.setMinimumHeight(int(self.py/10))

        self.setMaximumWidth(int(self.px*2))
        self.setMaximumHeight(int(self.py*2))

    def paintEvent(self, event: QResizeEvent):
        if not self.pixmap.isNull() and self.fp != "":
            self.image_update()

    def image_update(self):
        # Painter instead of label for resizing
        painter = QPainter(self)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)
        # Minimum scale to keep aspect ratio
        sclmin = np.min([self.rect().width(), self.rect().height()])
        # Original scale and position
        scl = [sclmin/(self.py/self.px), sclmin]
        pos = [self.rect().x(), self.rect().y()]
        # Position adjusted for centering image
        pos[0] += (self.rect().width()/2) - (scl[0]/2)
        pos[1] += (self.rect().height()/2) - (scl[1]/2)
        # Draw
        rect = QRect(int(pos[0]), int(pos[1]), int(scl[0]), int(scl[1]))
        painter.drawPixmap(rect, self.pixmap)

    

class OptionsMenu(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.setParent(parent)

        # Variables
        self.dither_mode = 0  # 0=None, 1=Threshold, 2=Halftone, 3=Bayer, 4=Floyd Steinberg, 5=Sierra
        self.scan_mode = 0    # 0=Horizontal, 1=Vertical
        self.inverted = False
        self.resize_fact_x = 1.0
        self.resize_fact_y = 1.0
        self.save_format = ""

        # Layout Formatting
        self.layout = QGridLayout()
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Minimum)

        # Load Image
        self.load = QPushButton()
        self.load.setText("Load Image...")
        self.load.clicked.connect(self.open_image)
        self.layout.addWidget(self.load, 1, 0, 1, 2)

        # Resize X
        self.resize_x = QLineEdit()
        self.resize_x.setText("1")
        
        self.resize_x_label = QLabel("Resize X:")
        self.resize_x_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout.addWidget(self.resize_x_label, 3, 0)

        self.layout.addWidget(self.resize_x, 3, 1, 1, 1)

        # Resize Y
        self.resize_y = QLineEdit()
        self.resize_y.setText("1")

        self.resize_y_label = QLabel("Resize Y:")
        self.resize_y_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout.addWidget(self.resize_y_label, 4, 0)

        self.layout.addWidget(self.resize_y, 4, 1, 1, 1)

        # Scan Direction
        self.scan = QComboBox(self)
        self.scan.addItem("Horizontal")
        self.scan.addItem("Vertical")

        self.scan_label = QLabel("Scan:")
        self.scan_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout.addWidget(self.scan_label, 5, 0)

        self.layout.addWidget(self.scan, 5, 1, 1, 1)

        # Invert Colors
        self.invert = QCheckBox()
        self.invert.setFocusPolicy(Qt.NoFocus)

        self.scan_label = QLabel("Invert:")
        self.scan_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout.addWidget(self.scan_label, 6, 0)

        self.layout.addWidget(self.invert, 6, 1, 1, 2)

        # Dithering Type
        self.dither = QComboBox(self)
        self.dither.addItem("None")
        self.dither.addItem("Threshold")
        self.dither.addItem("Halftone")
        self.dither.addItem("Bayer")
        self.dither.addItem("Floyd–Steinberg (SLOW)")
        self.dither.addItem("Sierra (SLOW)")

        self.dither_label = QLabel("Dithering:")
        self.dither_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout.addWidget(self.dither_label, 7, 0)

        self.layout.addWidget(self.dither, 7, 1, 1, 1)

        # Save Type
        self.save_type = QComboBox(self)
        self.save_type.addItem("C File (*.c)")
        self.save_type.addItem("Header File (*.h)")
        self.save_type.addItem("Text File (*.txt)")
        self.save_type.addItem("Image File (*.png)")

        self.save_type_label = QLabel("Save Type:")
        self.save_type_label.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.layout.addWidget(self.save_type_label, 8, 0)

        self.layout.addWidget(self.save_type, 8, 1, 1, 1)

        # Update Image
        self.update_img = QPushButton()
        self.update_img.setText("Update Image...")
        self.update_img.clicked.connect(self.update_vals)
        self.layout.addWidget(self.update_img, 9, 0, 1, 2)

        # Save Bitmap
        self.save = QPushButton()
        self.save.setText("Save Bitmap...")
        self.save.clicked.connect(self.write_image)
        self.layout.addWidget(self.save, 10, 0, 1, 2)

        # Finish
        self.setLayout(self.layout)

    def open_image(self):
        home = expanduser("~")
        read_path = QFileDialog.getOpenFileName(
            self, 
            'Open Image File', 
            home+'\Downloads', 
            'Portable Network Graphic (*.png)\nJPEG/JPEG 2000 (*.jpeg, *.jpg, *.jpe, *.jp2)\nTIFF (*.tiff, *.tif)\nBitmap (*.bmp)\nPortable Image Format (*.pbm, *.pgm, *.ppm)\nSun Raster (*.sr, *.ras)'
            )
        if read_path[0] != "":
            self.parent().update_filehandler(read=read_path[0])

    def write_image(self):
        home = expanduser("~")
        save_type = self.save_type.currentText()
        write_path = QFileDialog.getSaveFileName(self, 'Open Image File', home+'\Downloads', save_type)
        if write_path[0] != "":
            self.parent().update_filehandler(write=write_path[0])
            self.parent().save_image()
    
    def update_vals(self):
        self.dither_mode = self.dither.currentIndex()

        self.inverted = self.invert.isChecked()

        self.scan_mode = self.scan.currentIndex()

        try:
            self.resize_fact_x = float(self.resize_x.text())
        except ValueError:
            self.resize_fact_x = 1

        try:
            self.resize_fact_y = float(self.resize_y.text())
        except ValueError:
            self.resize_fact_y = 1

        self.save_format = self.save_type.currentText()

        self.parent().ui_update()
        

# Main window
class App(QWidget):
    # Init
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image to Bitmap")
        # self.setGeometry(200, 200, 800, 400)

        self.window_gui()
    
    # All window GUI
    def window_gui(self):
        # Paths
        self.img1_path = ""
        self.img2_path = ""

        # Main Layout
        self.layout = QGridLayout()

        # Original Image
        self.img1 = ImageView(self.img1_path)
        self.layout.addWidget(self.img1, 0, 0, 1, 4)

        # Transformed Image (preview)
        self.img2 = ImageView(self.img2_path)
        self.layout.addWidget(self.img2, 0, 4, 1, 4)

        # Options Panel
        self.options_panel = OptionsMenu(self)
        self.layout.addWidget(self.options_panel, 0, 8, 1, 1)

        # File Handler
        self.fh = FileHandler(self.img1_path, None, "C:\\tmp")

        self.setLayout(self.layout)

    def update_filehandler(self, read=None, write=None, tmp=None):
        if read is not None: self.fh.read_path = read
        if write is not None: self.fh.write_path = write
        if tmp is not None: self.fh.tmp_path = tmp

        self.ui_update()
    
    def ui_update(self):
        if self.fh.read_path != "" and self.fh.read_path is not None:
            tmp_img = resize_image(self.fh.read_image(), self.options_panel.resize_fact_x, self.options_panel.resize_fact_y)
            
            if self.options_panel.inverted:
                tmp_img = 255-tmp_img
            
            dither = self.options_panel.dither_mode
            
            if dither == 1: tmp_img = linear_dither(tmp_img, LinearMatrix(np.array([[1], [1]]), (1/2)))
            if dither == 2: tmp_img = linear_dither(tmp_img, HALFTONE_MATRIX_5X5)
            if dither == 3: tmp_img = linear_dither(tmp_img, BAYER_MATRIX_4X4)
            if dither == 4: tmp_img = diffuse_dither(tmp_img, FLOYD_STEINBERG)
            if dither == 5: tmp_img = diffuse_dither(tmp_img, SIERRA)

            self.fh.write_tmp_image(tmp_img)
        
            self.img1.set_pixmap(self.fh.read_path)

            self.img2.set_pixmap(os.path.join(self.fh.tmp_path, "tmp.png"))
    
    def save_image(self):
        if (self.fh.write_path != "" and self.fh.write_path is not None):
            tmp_img = cv2.imread(os.path.join(self.fh.tmp_path, "tmp.png"))
            tmp_img = convert_colorspace(tmp_img, 2)
            

            if self.options_panel.save_format == "Image File (*.png)":
                print("saving png image to {}".format(self.fh.write_path))
                self.fh.write_bitmap_png(tmp_img)
            else:
                print("saving text image to {}".format(self.fh.write_path))
                self.fh.write_bitmap_txt(tmp_img, self.options_panel.scan_mode)




# Window setup and management
def window_init():
    app = QApplication(sys.argv)
    win = App()

    win.show()
    sys.exit(app.exec_())

# Main
def main():
    window_init()
    return

if __name__ == '__main__':
    main()
