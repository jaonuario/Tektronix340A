from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE, SerialException
from serial.tools import list_ports
import time
import datetime
import csv

class Tektronix():
    def __init__(self):
        self.ports = list_ports.comports()
        self.baudrate = 19200
        self.serial_port = None      
        self.ser = None          
        self.device_info = None
    
    def get_baudrate_list():
        return [1200, 2400, 4800, 9600, 19200]

    def get_list_ports():
        return [port.device for port in list_ports.comports()]

    def status(self):
        if not self.ser:
            return 2
        if not self.ser.isOpen():
            return 1
        return 0

    def start(self):
        if (len(self.ports) == 0):
            print('Erro: Não há portas disponiveis!')
            return
        
        if not self.serial_port:
            self.serial_port = Tektronix.get_list_ports()[0]
    
        if (self.ser is None):
            try:
                self.ser = Serial(
                    port=self.serial_port,
                    baudrate= self.baudrate,
                    bytesize=EIGHTBITS,
                    stopbits=STOPBITS_ONE
                )

            except SerialException as e:
                print(f'Falha ao conectar na porta {self.serial_port}: {e}')
                return 0 

        if (self.ser.isOpen()):
            time.sleep(0.5)
            self.ser.close()
        
        time.sleep(0.5)
        self.ser.open()
        return 1


    def close_port(self):
        if (self.ser is None):
            print('Erro: Porta serial não iniciada')
            return

        if (self.ser.isOpen()):
            self.ser.close()
        return

    def send_command(self, command:str):
        status = self.status()
        if status:
            print(f'Erro {status}')
            return
        try:
            self.ser.write(command.encode() + b'\n')
            time.sleep(0.1)
            if(command.strip().endswith('?')):
                return self.read_response()

        except SerialException as e:
            print(f'Falha em enviar {command}: {e}')
            return None

    def send_commands(self , commands:[str]):
        status = self.status()
        if status:
            print(f'Erro {status}')
            return

        out_list = []
        for cmd in commands:
            out = self.send_command(cmd)
            if out:
                out_list.append(out)

        return out_list if len(out_list) else None 

    def read_response(self):
        status = self.status()
        if status:
            print(f'Erro {status}')
            return 

        response = self.ser.readline().decode()
        self.ser.flush()
        return response

    def device_id(self):
        res = self.send_command('ID?')        
        if res:
            res = res.strip().split(',')
            return {
                "Model": res[0],
                "Seria Number": res[1],
                "Firmware Version": res[2]   
            }
        return None 

    def ch1_freq(self):
        CH1_FREQ = [
        "MEASU:IMM:SOURCE CH1",
        "MEASU:IMM:TYPE FREQ",
        "MEASU:IMM:VAL?"
        ]

        return self.send_commands(CH1_FREQ)        


    def ch2_freq(self):
        CH2_FREQ = [
        "MEASU:IMM:SOURCE CH2",
        "MEASU:IMM:TYPE FREQ",
        "MEASU:IMM:VAL?"
        ]
        
        return self.send_commands(CH2_FREQ)


    def ch1_waveform(self):
        CH1_WAVEFORM = [
            'DAT:SOU CH1',
            "DAT:ENC ASCI",    
            "DAT:WID 2",       
            "DAT:STAR 1",      
            "DAT:STOP 1000",   
            "WFMPR?",          
            "CURV?"            
        ]

        res = self.send_commands(CH1_WAVEFORM)
        if res:
            return Waveform(res[0], res[1]) 
        return None   

    def ch2_waveform(self):
        CH2_WAVEFORM = [
            'DAT:SOU CH2',
            "DAT:ENC ASCI",    
            "DAT:WID 2",       
            "DAT:STAR 1",      
            "DAT:STOP 1000",   
            "WFMPR?",          
            "CURV?"            
        ]

        res = self.send_commands(CH2_WAVEFORM)
        if res:
            return Waveform(res[0], res[1])
        return None

    def math_waveform(self):
        MATH_WAVEFORM = [
            'DAT:SOU MATH',
            "DAT:ENC ASCI",    
            "DAT:WID 2",       
            "DAT:STAR 1",      
            "DAT:STOP 1000",   
            "WFMPR?",          
            "CURV?"            
        ]

        res = self.send_commands(MATH_WAVEFORM)
        if res:
            return Waveform(res[0], res[1])
        return None

    def ref1_waveform(self):
        REF1_WAVEFORM = [
            'DAT:SOU REF1',
            "DAT:ENC ASCI",    
            "DAT:WID 2",       
            "DAT:STAR 1",      
            "DAT:STOP 1000",   
            "WFMPR?",          
            "CURV?"            
        ]

        res = self.send_commands(REF1_WAVEFORM)
        if res:
            return Waveform(header, payload)
        return None

    def ref2_waveform(self):
        REF2_WAVEFORM = [
            'DAT:SOU REF2',
            "DAT:ENC ASCI",    
            "DAT:WID 2",       
            "DAT:STAR 1",      
            "DAT:STOP 1000",   
            "WFMPR?",          
            "CURV?"            
        ]

        res = self.send_commands(REF2_WAVEFORM)
        if res:
            return Waveform(header, payload)
        return None

    def event_log(self):
        EVENT_LOG = [
            "*ESR?",
            "ALLE?"
        ]
        
        return self.send_commands(EVENT_LOG)


class Waveform:
    def __init__(self, wfmpr_response: str, curv_response: str = None):
        """
        Inicializa a classe com a resposta do comando WFMPR? e CURV?.
        
        Parâmetros:
            wfmpr_response (str): Resposta bruta do comando WFMPR?.
            curv_response (str, opcional): Resposta bruta do comando CURV?.
        """
        self.raw_data = wfmpr_response
        self.curv_data = curv_response
        self.parsed_data = self._parse_response()
    
    def _parse_response(self):
        """
        Processa a resposta do WFMPR? e retorna um dicionário com os parâmetros nomeados.
        """
        values = self.raw_data.split(';')
        return {
            "NUM_CHANNELS": int(values[0]),
            "BIT_DEPTH": int(values[1]),
            "ENCODING": values[2],
            "ACQUISITION_MODE": values[3],
            "BYTE_ORDER": values[4],
            "WAVEFORM_INFO": values[5].strip('"'),
            "NUM_POINTS": int(values[6]),
            "Y_UNIT": values[7],
            "X_UNIT": values[8].strip('"'),
            "XINCREMENT": float(values[9]),
            "XZERO": float(values[10]) * 1e-6,  # Convertendo para segundos
            "Y_UNIT_2": values[11].strip('"'),
            "YINCREMENT": float(values[12]),
            "YZERO": float(values[13]) * 1e-3,  # Convertendo para volts
            "YMULT": float(values[14])
        }
    
    def get_data(self):
        """
        Retorna os dados processados.
        """
        return self.parsed_data
    
    def get_raw_curv_data(self):
        """
        Retorna os dados brutos de CURV? como um array de inteiros.
        """
        if not self.curv_data:
            return None
        return list(map(int, self.curv_data.split(',')))

    def process_curv_data(self):
        """
        Processa os valores de CURV? e retorna uma lista de tensões convertidas.
        """
        if not self.curv_data:
            return None 
        
        data_points = list(map(int, self.curv_data.split(',')))
        y_increment = self.parsed_data["YINCREMENT"]
        y_zero = self.parsed_data["YZERO"]
        
        voltage_values = [y_zero + (y_increment * point) for point in data_points]
        return voltage_values

    def get_time_array(self):
        """
        Retorna um array de tempo correspondente aos pontos da forma de onda.
        """
        num_points = self.parsed_data["NUM_POINTS"]
        x_increment = self.parsed_data["XINCREMENT"]
        x_zero = self.parsed_data["XZERO"]
        
        time_values = [x_zero + i * x_increment for i in range(num_points)]
        return time_values

    def get_voltage_max(self):
        """
        Retorna o limite superior dos valores de CURV? convertidos em tensão.
        """
        bit_depth = self.parsed_data["BIT_DEPTH"]
        max_value = (2 ** (bit_depth - 1)) - 1  # Assumindo valores com sinal
        return self.parsed_data["YZERO"] + (self.parsed_data["YINCREMENT"] * max_value)
    
    def get_voltage_min(self):
        """
        Retorna o limite inferior dos valores de CURV? convertidos em tensão.
        """
        bit_depth = self.parsed_data["BIT_DEPTH"]
        min_value = -(2 ** (bit_depth - 1))  # Assumindo valores com sinal
        return self.parsed_data["YZERO"] + (self.parsed_data["YINCREMENT"] * min_value)

    def generate_csv(self, file_name=None):

        header = ['time', 'curv']
        curv = self.get_raw_curv_data()
        time = self.get_time_array()
        
        if not curv and not time:
            print('erro: curv ou time nao carregados')
            return

        data = [time, curv]
        data_t = [[linha[i] for linha in data] for i in range(len(data[0]))]

        if not file_name:
            file_name = str(datetime.datetime.now())
        
        csv_file = open(file_name.strip().replace(' ', '_') + '.csv', 'w')
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(data_t)
        csv_file.close()
        pass

    def generate_waveform_txt(self, name=None):
        if not name:
            name = str(datetime.datetime.now()).strip().replace(' ', '_').replace('.','_')

        file = open(name + '.txt', 'w')
        file.write(self.raw_data)
        file.write(self.curv_data)
        file.close()
        pass
    
    @staticmethod
    def build_waveform_by_txt(file_name:str):
        if not file_name.endswith('.txt'):
            print('tipo de arquivo inválido')
        
        file = open(file_name, 'r')
        header = file.readline()
        curv = file.readline()

        return Waveform(header, curv)
        pass

    def __str__(self):
        """
        Retorna uma representação formatada dos dados processados.
        """
        return "\n".join(f"{key}: {value}" for key, value in self.parsed_data.items())
    

import numpy as np
import matplotlib.pyplot as plt

def plot_xy(x, y, y_min=None, y_max=None):
    """
    Plota um gráfico a partir de dois arrays de números float representando os eixos x e y.
    
    Parâmetros:
    x (list of float): Lista de números float para o eixo X.
    y (list of float): Lista de números float para o eixo Y.
    y_min (float, opcional): Valor mínimo para o eixo Y.
    y_max (float, opcional): Valor máximo para o eixo Y.
    
    Retorno:
    None
    """
    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker='o', linestyle='-', color='b', label='Valores')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title('Plot de X vs Y')
    
    if y_min is not None and y_max is not None:
        plt.ylim(y_min, y_max)
    
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    #tek = Tektronix()
    #tek.start()
    
    #waveform = tek.ch1_waveform()
    waveform = Waveform.build_waveform_by_txt('2025-02-11_15:20:28_199721.csv')
    print(waveform)
    
    if waveform:
        x = waveform.get_time_array()
        y = waveform.process_curv_data()
        y_max = waveform.get_voltage_max()
        y_min = waveform.get_voltage_min()

        plot_xy(x, y, y_min, y_max)
        #waveform.generate_csv()
        #waveform.generate_waveform_txt()    
    
    pass
