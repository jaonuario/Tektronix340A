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

        model_label = qt.QLabel('model', parent=self)
        model_text = qt.QLineEdit('model', parent=self)
        model_text.setReadOnly(True)
        model_text.setObjectName('model')

        serial_number_label = qt.QLabel('serial_number', parent=self)
        serial_number_text = qt.QLineEdit('serial_number', parent=self)
        serial_number_text.setReadOnly(True)
        serial_number_text.setObjectName('serial_number')

        firmware_label = qt.QLabel('firmware', parent=self)
        firmware_text = qt.QLineEdit('firmware', parent=self)
        firmware_text.setReadOnly(True)
        firmware_text.setObjectName('firmware')
                
        bdt_label = qt.QLabel('Baudrate', parent=self)
        baudrate = qt.QComboBox(self)
        baudrate.setObjectName('baudrate')
        
        port_label = qt.QLabel('Port: ', parent=self)
        port = qt.QComboBox(self)
        port.setObjectName('port')
        
        #grid config
        grid_layout.setVerticalSpacing(20)
        grid_layout.addWidget(model_label, 1, 0)
        grid_layout.addWidget(model_text, 1, 1)
        grid_layout.addWidget(serial_number_label, 2, 0)
        grid_layout.addWidget(serial_number_text, 2, 1)
        grid_layout.addWidget(firmware_label, 3, 0)
        grid_layout.addWidget(firmware_text, 3, 1)
        grid_layout.addWidget(bdt_label, 4, 0)
        grid_layout.addWidget(baudrate, 4, 1)
        grid_layout.addWidget(port_label, 5, 0)        
        grid_layout.addWidget(port, 5, 1)        

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

    def set_model_value(self, value:str)->None:
        model:qt.QLineEdit = self.findChild(qt.QLineEdit, name='model')
        model.setText(value)

    def set_serial_number_value(self, value:str)->None:
        serial_number:qt.QLineEdit = self.findChild(qt.QLineEdit, name='serial_number')
        serial_number.setText(value)

    def set_firmware_value(self, value:str)->None:
        firmware:qt.QLineEdit = self.findChild(qt.QLineEdit, name='firmware')
        firmware.setText(value)



if __name__ == "__main__":
    # Criação da aplicação
    app = qt.QApplication(sys.argv)

    # Criação da janela principal
    window = FormsWidget()
    window.show()

    # Executar o loop da aplicação
    sys.exit(app.exec())
