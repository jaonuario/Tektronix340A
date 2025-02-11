import sys
import numpy as np
import PySide6.QtWidgets as qt
import PySide6.QtGui as gui

from AppWidget import AppWidget
from Tektronix import Tektronix

class App(qt.QMainWindow):
    def __init__(self):
        super().__init__()

        self.central_widget = AppWidget()
        self.setCentralWidget(self.central_widget)

        self.tektronix = Tektronix()
        self.central_widget.infos.set_baudrate_values(list(map(str, Tektronix.get_baudrate_list())))
        self.central_widget.infos.set_port_values(self.tektronix.ports)

        self.config_conections()
        self.initialize()
    
    def initialize(self):
        self.central_widget.workspace.set_logstream()
        pass

    def config_conections(self):
        button = self.central_widget.workspace.get_all_buttons()

        button['open_port'].clicked.connect(self.start_device())
        button['device_id'].clicked.connect(self.device_id)
        button['ch1_freq'].clicked.connect(self.ch1_freq)
        button['ch2_freq'].clicked.connect(self.ch2_freq)
        button['ch1_waveform'].clicked.connect(self.ch1_waveform)
        button['ch2_waveform'].clicked.connect(self.ch2_waveform)
        button['math_waveform'].clicked.connect(self.math_waveform)
        button['ref1_waveform'].clicked.connect(self.ref1_waveform)
        button['ref2_waveform'].clicked.connect(self.ref2_waveform)
        button['event_log'].clicked.connect(self.event_log)

    def start_device(self):
        if self.tektronix.start():
            self.get_device_id()

    def get_device_id(self):
        id = self.tektronix.device_id()
        if id:
            self.central_widget.infos.set_model_value(id["Model"])
            self.central_widget.infos.set_serial_number_value(id["Seria Number"])
            self.central_widget.infos.set_firmware_value(id["Firmware Version"])
    
    def device_id(self):
        print(self.tektronix.device_id())

    def ch1_freq(self):
        print(self.tektronix.ch1_freq())

    def ch2_freq(self):
        print(self.tektronix.ch2_freq())

    def ch1_waveform(self):
        waveform = self.tektronix.ch1_waveform()
        self.__plotwaveform(waveform=waveform)

    def ch2_waveform(self):
        waveform = self.tektronix.ch2_waveform()
        self.__plotwaveform(waveform=waveform)

    def math_waveform(self):
        print('math waveform')
        x = np.linspace(0,10,100)
        y = np.sin(x)
        self.central_widget.workspace.plot(x, y)

    def ref1_waveform(self):
        waveform = self.tektronix.ref1_waveform()
        self.__plotwaveform(waveform=waveform)

    def ref2_waveform(self):
        waveform = self.tektronix.ref2_waveform()
        self.__plotwaveform(waveform=waveform)

    def __plotwaveform(self, waveform):
        if waveform:
            curv = waveform.process_curv_data()
            time = waveform.get_time_array()
            v_max = waveform.get_voltage_max()
            v_min = waveform.get_voltage_min()
            self.central_widget.workspace.plot(time, curv, v_max, v_min)

    def event_log(self):
        for res in self.tektronix.event_log():
            print(res)

if __name__ == "__main__":
    # Criação da aplicação
    app = qt.QApplication(sys.argv)

    # Criação da janela principal
    window = App()
    window.show()

    # Executar o loop da aplicação
    sys.exit(app.exec())

