import sys
import io
import PySide6.QtWidgets as qt
import PySide6.QtGui as gui

from WSWidget import WSWidget
from FormsWidget import FormsWidget

class AppWidget(qt.QWidget):
    def __init__(self, parent=None, title='App'):
        super().__init__(parent=parent)
        
        tabs = qt.QTabWidget(self)
        
        tabs.addTab(WSWidget(parent=self), 'workspace')
        tabs.addTab(FormsWidget(parent=self), 'infos')

        layout = qt.QVBoxLayout(self)
        layout.addWidget(tabs)

        self.setLayout(layout)
        #self.setFixedSize(600, 800)
        self.setWindowTitle(title)


    def get_all_buttons(self)->dict[str:qt.QPushButton]:
        return self.findChild(WSWidget).get_all_buttons()

    def set_baudrate_values(self, value:[str])->None:
        widget:FormsWidget = self.findChild(FormsWidget)
        widget.set_baudrate_values(value)

    def set_port_values(self, value:[str])->None:
        widget:FormsWidget = self.findChild(FormsWidget)
        widget.set_port_values(value)

    def set_version_value(self, value:str)->None:
        widget:FormsWidget = self.findChild(FormsWidget)
        widget.set_version_value(value)

    def set_name_value(self, value:str)->None:
        widget:FormsWidget = self.findChild(FormsWidget)
        widget.set_name_value(value)


if __name__ == "__main__":
    # Criação da aplicação
    app = qt.QApplication(sys.argv)

    # Criação da janela principal
    window = AppWidget()
    window.show()

    print(window.get_all_buttons())
    # Executar o loop da aplicação
    sys.exit(app.exec())

