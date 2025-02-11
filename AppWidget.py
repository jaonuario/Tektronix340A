import sys
import io
import PySide6.QtWidgets as qt
import PySide6.QtGui as gui

from WSWidget import WSWidget
from FormsWidget import FormsWidget

class AppWidget(qt.QWidget):
    def __init__(self, parent=None, title='App'):
        super().__init__(parent=parent)
        
        self.workspace = WSWidget(parent=self)
        self.infos = FormsWidget(parent=self)
        tabs = qt.QTabWidget(self)
        tabs.addTab(self.workspace, 'workspace')
        tabs.addTab(self.infos, 'infos')

        layout = qt.QVBoxLayout(self)
        layout.addWidget(tabs)

        self.setLayout(layout)
        self.setWindowTitle(title)


if __name__ == "__main__":
    # Criação da aplicação
    app = qt.QApplication(sys.argv)

    # Criação da janela principal
    window = AppWidget()
    window.show()

    # Executar o loop da aplicação
    sys.exit(app.exec())

