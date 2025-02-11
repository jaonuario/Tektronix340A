import sys
import io
import PySide6.QtWidgets as qt
import PySide6.QtGui as gui
from Util import PlotWidget

import numpy as np

class WSWidget(qt.QWidget):
    def __init__(self, parent=None, name="workspace"):
        super().__init__(parent=parent)
        
        #layouts
        self.main_layout = qt.QVBoxLayout()
        self.info_area = qt.QVBoxLayout()
        self.workspace_area = qt.QHBoxLayout()
        self.dev_area = qt.QVBoxLayout()

        #layout config
        self.config_workspace_area()
        self.config_dev_area()

        self.main_layout.addLayout(self.info_area)
        self.main_layout.addLayout(self.workspace_area)
        self.main_layout.addLayout(self.dev_area)

        #Configurações do widget
        self.setWindowTitle(name)
        self.setLayout(self.main_layout)
        self.setSizePolicy(qt.QSizePolicy.Expanding, qt.QSizePolicy.Expanding)


    def config_workspace_area(self):
        self.workspace_area.addLayout(self.button_grid_layout())
        self.workspace_area.addLayout(self.display_area())


    def config_dev_area(self):
        self.dev_area.addLayout(self.custom_commands())

        self.log_output = qt.QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setPlaceholderText("Logs aparecerão aqui...")
        
        self.dev_area.addWidget(self.log_output)


    def button_grid_layout(self):
        #button grid
        button_grid = qt.QVBoxLayout()

        button_grid.addWidget(self.create_button('Open Port'))
        button_grid.addWidget(self.create_button('Device ID'))
        button_grid.addWidget(self.create_button('CH1 Freq'))
        button_grid.addWidget(self.create_button('CH2 Freq'))
        button_grid.addWidget(self.create_button('CH1 Waveform'))
        button_grid.addWidget(self.create_button('CH2 Waveform'))
        button_grid.addWidget(self.create_button('Math Waveform'))
        button_grid.addWidget(self.create_button('Ref1 Waveform'))
        button_grid.addWidget(self.create_button('Ref2 Waveform'))
        button_grid.addWidget(self.create_button('Event Log'))

        return button_grid


    def display_area(self):
        layout = qt.QVBoxLayout()

        # Imagem
        plot = PlotWidget(self)

        # Layout horizontal com botões
        button_layout = qt.QHBoxLayout()
        sshot = self.create_button("Screenshot")
        save = self.create_button("Save")
        clear = self.create_button("Clear")

        button_layout.addWidget(sshot)
        button_layout.addWidget(save)
        button_layout.addWidget(clear)

        # Adicionar componentes ao layout vertical
        layout.addWidget(plot, stretch=1)
        layout.addLayout(button_layout)

        return layout


    def custom_commands(self):
        layout = qt.QGridLayout()

        # Elementos do grid
        label_1 = qt.QLabel("Label 1:")
        self.line_edit = qt.QLineEdit()
        btn1 = self.create_button("Button 1")
        label_2 = qt.QLabel("Label 2:")
        btn2 = self.create_button("Button 2")

        # Adicionar ao grid layout
        layout.addWidget(label_1, 0, 0)
        layout.addWidget(self.line_edit, 0, 1)
        layout.addWidget(btn1, 0, 2)
        layout.addWidget(label_2, 1, 0)
        layout.addWidget(btn2, 1, 2)

        return layout


    def get_all_buttons(self) -> dict[str:qt.QPushButton]:
        btns = self.findChildren(qt.QPushButton)
        return {btn.objectName() : btn for btn in btns if btn.objectName()}
        
        
    def create_button(self, name):
        btn = qt.QPushButton(name, parent=self)
        btn.setObjectName(name.lower().replace(' ', '_'))
        return btn

    def plot(self, x, y, y_min=None, y_max=None):
        plt = self.findChild(PlotWidget)
        plt.plot(x,y,y_min,y_max)

    def set_logstream(self):
        sys.stdout = LogStream(self.log_output)
        sys.stderr = LogStream(self.log_output)
        
class LogStream(io.StringIO):
    """Classe para redirecionar sys.stdout e sys.stderr para um widget PyQt."""
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def write(self, message):
        """Escreve a mensagem no QTextEdit."""
        self.text_widget.append(message.strip())

    def flush(self):
        """Flush não faz nada, mas é necessário para compatibilidade."""
        pass



if __name__ == "__main__":
    # Criação da aplicação
    app = qt.QApplication(sys.argv)

    # Criação da janela principal
    window = WSWidget()
    window.show()

    # Executar o loop da aplicação
    sys.exit(app.exec())
