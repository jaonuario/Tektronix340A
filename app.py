import sys
import os
import logging

# PyQt
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QPushButton, QTextEdit, QLineEdit, QFileDialog, QComboBox
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFont
from pyqtgraph import PlotWidget

# Source
from src import Waveform
from src import Tektronix

# Configuração básica do logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Main:
    def __init__(self):
        """Inicializa a classe Main e configura a interface do usuário."""
        logger.debug("Initializing Main class")
        
        # Loader config
        loader = QUiLoader()
        loader.registerCustomWidget(PlotWidget)
        self.ui = loader.load("ui/mainwindow.ui")

        if not self.ui:
            logger.error("Failed to load UI file.")
            sys.exit(1)

        self.tektronix = Tektronix()

        self.config_informations()
        self.plot_config()
        self.connect_buttons()
        self.waveform: Waveform = None  # Atributo para armazenar a waveform atual
        self.buttons_enabled = True     # Flag para controlar o estado dos botões

        # Exemplo de carregamento de waveform (comentado para evitar execução automática)
        waveform = Waveform.from_file('2025-02-11_15:48:57_142614.txt')
        self.show_waveform(waveform)
        
        self.windown_config()
        self.tektronix.start()
    
    def run(self):
        """Executa a aplicação, exibindo a janela principal."""
        logger.debug("Running application")
        self.ui.show()

    # Métodos de Configuração
    def windown_config(self):
        """Configura as propriedades da janela principal, como título e fontes."""
        logger.debug("Configuring window settings")
        self.ui.setWindowTitle("Waveform Viewer")
        display: QTextEdit = self.ui.findChild(QTextEdit, name="ResultArea")
        if display:
            display.setFont(QFont("Courier", 12))
        
        combox:QComboBox = self.ui.findChild(QComboBox, name="TypeFile")
        if not combox:
            logger.warning("Combox not found")
            return

        combox.addItems(["txt", "csv"])        

    def config_informations(self):
        """Configura as informações do dispositivo na interface do usuário."""
        logger.debug("Configuring additional information")
        line_edit = {line.objectName(): line for line in self.ui.findChildren(QLineEdit) if line.objectName()}
        infos = self.tektronix.device_id()

        if not infos:
            logger.error("Infos not found")
            return   

        if not line_edit:
            logger.error("LineEdit not found")
            return   

        line_edit["Model"].setText(infos["Model"])
        line_edit["Serial Number"].setText(infos["Serial Number"])
        line_edit["Firmware"].setText(infos["Firmware Version"])

    def log_config(self):
        """Configurações personalizadas de logging, se necessário."""
        logger.debug("Configuring logging settings")
        pass

    def plot_config(self):
        """Configura o widget de plotagem."""
        logger.debug("Configuring plot settings")
        plot_graph: PlotWidget = self.ui.findChild(PlotWidget)
        if plot_graph:
            plot_graph.setMouseEnabled(x=False, y=False)
            logger.info("PlotWidget configured")
        else:
            logger.error("PlotWidget not found")

    # Métodos de Apoio
    def show_waveform(self, waveform: Waveform):
        """Exibe a waveform no widget de plotagem."""
        self.waveform_log(waveform)
        if not waveform:
            logger.error("Waveform not found")
            return

        self.waveform = waveform
        logger.debug("Displaying waveform")
        plot_graph: PlotWidget = self.ui.findChild(PlotWidget)
        if not plot_graph:
            logger.error("PlotWidget not found")
            return

        margin = 10
        y_upper_limit = waveform.get_voltage_max()
        y_lower_limit = waveform.get_voltage_min()
        if y_lower_limit is not None and y_upper_limit is not None:
            plot_graph.setYRange(y_lower_limit - margin, y_upper_limit + margin)

        curv_data = waveform.process_curv_data()
        time = waveform.get_time_array()

        plot_graph.plot(time, curv_data)
        logger.info("Waveform displayed successfully")

    def writer_console(self, value: str):
        """Escreve um valor na área de texto de resultados, limpando o console antes."""
        self.clear_console()  # Limpa o console antes de escrever
        display: QTextEdit = self.ui.findChild(QTextEdit, name="ResultArea")
        if not display:
            logger.error("QTextEdit not found")
            return
        display.append(value)

    def clear_console(self):
        """Limpa a área de texto de resultados."""
        display: QTextEdit = self.ui.findChild(QTextEdit, name="ResultArea")
        display.clear()

    def clear_waveform(self):
        """Limpa a waveform exibida no widget de plotagem."""
        logger.debug("Clear Waveform button clicked")
        plot_graph: PlotWidget = self.ui.findChild(PlotWidget)
        if plot_graph:
            plot_graph.clear()
            logger.info("Waveform cleared")
        else:
            logger.error("PlotWidget not found")
    
    def waveform_log(self, waveform: Waveform):
        """Exibe os dados da waveform em formato de tabela na área de texto de resultados."""
        if not waveform:
            logger.error("Waveform not found")
            return

        dictionary = waveform.get_waveform_data()

        # Determina a largura das colunas
        key_width = max(len(str(key)) for key in dictionary.keys())
        value_width = max(len(str(value)) for value in dictionary.values())

        # Cria a linha de separação
        separator = '+' + '-' * (key_width + 2) + '+' + '-' * (value_width + 2) + '+'

        # Cria o cabeçalho da tabela
        table = separator + '\n'
        table += '| {:<{}} | {:<{}} |\n'.format('Key', key_width, 'Value', value_width)
        table += separator + '\n'

        # Adiciona as linhas com os dados do dicionário
        for key, value in dictionary.items():
            table += '| {:<{}} | {:<{}} |\n'.format(str(key), key_width, str(value), value_width)

        # Fecha a tabela com a linha de separação
        table += separator
        
        self.writer_console(table)

    # Slots
    def connect_buttons(self):
        """Conecta os botões da interface aos seus respectivos métodos."""
        logger.debug("Connecting buttons to their respective methods")
        buttons: dict[str: QPushButton] = {btn.objectName(): btn for btn in self.ui.findChildren(QPushButton) if btn.objectName()}

        if not buttons:
            logger.warning("No buttons found in the UI.")

        # Conecta cada botão ao seu método correspondente
        buttons['CH1Freq'].clicked.connect(self.ch1_freq)
        buttons['CH2Freq'].clicked.connect(self.ch2_freq)
        buttons['CH1Waveform'].clicked.connect(self.ch1_waveform)
        buttons['CH2Waveform'].clicked.connect(self.ch2_waveform)
        buttons['MathWaveform'].clicked.connect(self.math_waveform)
        buttons['MathWaveform'].setEnabled(False)  # TODO: Resolver o bug desse comando
        buttons['Ref1Waveform'].clicked.connect(self.ref1_waveform)
        buttons['Ref2Waveform'].clicked.connect(self.ref2_waveform)
        buttons['Save'].clicked.connect(self.save_waveform)
        buttons['Clear'].clicked.connect(self.clear_all)

    def ch1_freq(self):
        """Exibe a frequência do canal 1 na área de texto de resultados."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("CH1 Frequency button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.writer_console(self.tektronix.ch1_freq())
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def ch2_freq(self):
        """Exibe a frequência do canal 2 na área de texto de resultados."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("CH2 Frequency button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.writer_console(self.tektronix.ch2_freq())
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def ch1_waveform(self):
        """Exibe a waveform do canal 1 no widget de plotagem e armazena no atributo."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("CH1 Waveform button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.clear_all()  # Limpa o console e o display antes de exibir a nova waveform
            self.waveform = self.tektronix.ch1_waveform()  # Armazena a waveform no atributo
            self.writer_console(str(self.tektronix.event_log()))
            self.show_waveform(self.waveform)
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def ch2_waveform(self):
        """Exibe a waveform do canal 2 no widget de plotagem e armazena no atributo."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("CH2 Waveform button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.clear_all()  # Limpa o console e o display antes de exibir a nova waveform
            self.waveform = self.tektronix.ch2_waveform()  # Armazena a waveform no atributo
            self.writer_console(str(self.tektronix.event_log()))
            self.show_waveform(self.waveform)
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def math_waveform(self):
        """Exibe a waveform matemática no widget de plotagem e armazena no atributo."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("Math Waveform button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.clear_all()  # Limpa o console e o display antes de exibir a nova waveform
            self.waveform = self.tektronix.math_waveform()  # Armazena a waveform no atributo
            self.writer_console(str(self.tektronix.event_log()))
            self.show_waveform(self.waveform)
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def ref1_waveform(self):
        """Exibe a waveform de referência 1 no widget de plotagem e armazena no atributo."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("Ref1 Waveform button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.clear_all()  # Limpa o console e o display antes de exibir a nova waveform
            self.waveform = self.tektronix.ref1_waveform()  # Armazena a waveform no atributo
            self.writer_console(str(self.tektronix.event_log()))
            self.show_waveform(self.waveform)
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def ref2_waveform(self):
        """Exibe a waveform de referência 2 no widget de plotagem e armazena no atributo."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("Ref2 Waveform button clicked")
        self.buttons_enabled = False  # Desativa a flag
        try:
            self.clear_all()  # Limpa o console e o display antes de exibir a nova waveform
            self.waveform = self.tektronix.ref2_waveform()  # Armazena a waveform no atributo
            self.writer_console(str(self.tektronix.event_log()))
            self.show_waveform(self.waveform)
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def save_waveform(self):
        """Salva a waveform atual em um arquivo."""
        if not self.buttons_enabled:
            return  # Ignora o evento se a flag estiver desativada
        logger.debug("Save Waveform button clicked")
        
        combox:QComboBox = self.ui.findChild(QComboBox, name="TypeFile")
        if not combox:
            logger.warning("Combox not found")
            return

        text_type = combox.currentText()
        user_home = os.path.expanduser("~")
        selected_directory = QFileDialog.getExistingDirectory(
            self.ui,
            "Selecione um diretório",
            user_home,
            QFileDialog.Option.ShowDirsOnly
        )

        self.buttons_enabled = False  # Desativa a flag
        try:
            if self.waveform:
                self.waveform.save_to_file(file_format=text_type, output_dir=selected_directory)
                self.writer_console("Waveform saved to waveform.txt")
            else:
                self.writer_console("No waveform to save")
        finally:
            self.buttons_enabled = True  # Reativa a flag

    def clear_all(self):
        """Limpa o console e o display de waveform."""
        self.clear_console()
        self.clear_waveform()

if __name__ == "__main__":
    logger.debug("Starting application")
    app = QtWidgets.QApplication(sys.argv)
    main = Main()
    main.run()
    sys.exit(app.exec())