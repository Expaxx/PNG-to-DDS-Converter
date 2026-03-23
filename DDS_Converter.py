from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QFileDialog, QMainWindow, QWidget
from PyQt6.QtCore import QSize

import os
import subprocess
import sys

#Create window
#Button for texconv
#Button for PNG folder
#New folder for DDS textures

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        #Button titles
        self.setWindowTitle("DDS Converter")
        button_texconv = QPushButton("Get texconv.exe")
        button_png_folder = QPushButton("Get PNG folder")

        #Setting button size
        button_texconv.setFixedSize(QSize(200,200))
        button_png_folder.setFixedSize(QSize(200,200))
        
        # Layout for buttons
        layout = QVBoxLayout()
        layout.addWidget(button_texconv)
        layout.addWidget(button_png_folder)

        #Button functionality
        button_texconv.clicked.connect(self.texConvEvent)
        button_png_folder.clicked.connect(self.pngFolderEvent)

        #Container for layout
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def texConvEvent(self):
        texConvFetch, _ = QFileDialog.getOpenFileName(self, "Select texconv.exe",
        "", 
        "Executable file (*exe);; All files (*)")

        if texConvFetch:
            self.texConv_Final = texConvFetch.replace("\\", "/")
            print("texconv.exe found!")
        else:
            print("texconv.exe not found!")

    def pngFolderEvent(self):
        self.pngFolderFetch = QFileDialog.getExistingDirectory(self, "Select PNG Folder")
        self.convertToDDS(self.pngFolderFetch)
    
    def convertToDDS(self, input_folder):
        output_path = os.path.join(input_folder, "OUT_DDS")
        os.makedirs(output_path, exist_ok = True)

        for file in os.listdir(input_folder):
            if file.endswith(".png"):
                full_input_path = os.path.join(input_folder, file)
                if file.endswith("_C.png") or file.endswith("_M.png"):
                    subprocess.run([
                        self.texConv_Final,
                        "-f", "BC7_UNORM", # -f = format, BC7_UNORM = image conversion type
                        "-o", output_path, full_input_path # -o = output
                    ])
                        
                elif file.endswith("_N.png"):
                    subprocess.run([
                        self.texConv_Final,
                        "-f", "BC5_UNORM",
                        "-o", output_path, full_input_path
                    ])
                    
                else:
                    print("failed operation")
            else:
                print("Cancelled operation")



app = QApplication(sys.argv)

window = MyWindow()
window.show()

sys.exit(app.exec())
