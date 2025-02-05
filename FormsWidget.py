import sys
import io
import PySide6.QtWidgets as qt
import PySide6.QtGui as qgui
from PySide6.QtCore import Qt

class FormsWidget(qt.QWidget):
    def __init__(self, parent:qt.QWidget=None, title:str='FormsWidget'):
        super().__init__(parent=parent)

        #widgets
        main_layout = qt.QVBoxLayout(self)
        grid_layout = qt.QGridLayout(self)
        
        name_label = qt.QLabel('Name', parent=self)
        name_text = qt.QLineEdit('Name', parent=self)
        name_text.setReadOnly(True)
        name_text.setObjectName('name')
        
        version_label = qt.QLabel('Version', parent=self)
        version_text = qt.QLineEdit('0.0.0.0', parent=self)
        version_text.setReadOnly(True)
        version_text.setObjectName('version')
        
        bdt_label = qt.QLabel('Baudrate', parent=self)
        baudrate = qt.QComboBox(self)
        baudrate.setObjectName('baudrate')
        
        port_label = qt.QLabel('Port: ', parent=self)
        port = qt.QComboBox(self)
        port.setObjectName('port')
        
        #grid config
        grid_layout.setVerticalSpacing(20)
        grid_layout.addWidget(name_label, 0, 0)
        grid_layout.addWidget(name_text, 0 , 1)
        grid_layout.addWidget(version_label, 1, 0)
        grid_layout.addWidget(version_text, 1, 1)
        grid_layout.addWidget(bdt_label, 2, 0)
        grid_layout.addWidget(baudrate, 2, 1)
        grid_layout.addWidget(port_label, 3, 0)
        grid_layout.addWidget(port, 3, 1)

        main_layout.addLayout(grid_layout)
        main_layout.addStretch(1)
        
        #self.setFixedSize(600, 800)
        self.setWindowTitle(title)
        self.setLayout(main_layout)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)

    
    def set_baudrate_values(self, values:[str])->None:
        box:qt.QComboBox = self.findChild(qt.QComboBox, name='baudrate')
        box.addItems(values)

    def set_port_values(self, values:[str])->None:
        box:qt.QComboBox = self.findChild(qt.QComboBox, name='port')
        box.addItems(values)

    def set_version_value(self, value:str)->None:
        version:qt.QLineEdit = self.findChild(qt.QLineEdit, name='version')
        version.setText(value)

    def set_name_value(self, value:str)->None:
        name:qt.QLineEdit = self.findChild(qt.QLineEdit, name='name')
        name.setText(value)



if __name__ == "__main__":
    # Criação da aplicação
    app = qt.QApplication(sys.argv)

    # Criação da janela principal
    window = FormsWidget()
    window.show()

    # Executar o loop da aplicação
    sys.exit(app.exec())
