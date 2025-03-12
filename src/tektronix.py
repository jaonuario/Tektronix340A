import time
import datetime
import csv
import logging
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE, SerialException
from serial.tools import list_ports
from .waveform import Waveform, WaveformPlot

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tektronix.log'),  # Log para arquivo
        logging.StreamHandler()               # Log para o console
    ]
)
logger = logging.getLogger('Tektronix')

class Tektronix():
    def __init__(self):
        self.baudrate = 19200
        self.serial_port = None
        self.ser = None
        self.device_info = None
        logger.info('Objeto Tektronix inicializado')

    @staticmethod
    def get_baudrate_list()->[int]:
        logger.debug('Lista de baudrates solicitada')
        return [1200, 2400, 4800, 9600, 19200]
    
    @staticmethod
    def get_list_ports()->[str]:
        logger.debug('Lista de portas seriais solicitada')
        return [port.device for port in list_ports.comports()]

    def status(self)->int:
        if not self.ser:
            logger.warning('Porta serial não inicializada')
            return 2
        if not self.ser.isOpen():
            logger.warning('Porta serial não está aberta')
            return 1
        return 0

    def start(self) -> int:
        ports_list = Tektronix.get_list_ports()
        if not ports_list:
            logger.error('Não há portas seriais disponíveis')
            return 0
        
        if not self.serial_port:
            self.serial_port = ports_list[0]
            logger.info(f'Porta serial selecionada: {self.serial_port}')
    
        if self.ser is None:
            try:
                self.ser = Serial(
                    port=self.serial_port,
                    baudrate=self.baudrate,
                    bytesize=EIGHTBITS,
                    stopbits=STOPBITS_ONE
                )
                logger.info('Conexão serial estabelecida com sucesso')
            except SerialException as e:
                logger.error(f'Falha ao conectar na porta {self.serial_port}: {e}')
                return 0

        if self.ser.isOpen():
            time.sleep(0.5)
            self.ser.close()
            logger.info('Porta serial fechada temporariamente')
        
        time.sleep(0.5)
        self.ser.open()
        logger.info('Porta serial reaberta')
        
        return 1

    def close_port(self):
        if self.ser is None:
            logger.error('Porta serial não inicializada')
            return

        if self.ser.isOpen():
            self.ser.close()
            logger.info('Porta serial fechada')
        return

    def send_command(self, command:str) -> str:
        status = self.status()
        if status:
            logger.error(f'Erro {status} ao enviar comando: {command}')
            return ''
        try:
            self.ser.write(command.encode() + b'\n')
            time.sleep(0.1)
            if command.strip().endswith('?'):
                response = self.read_response()
                logger.debug(f'Comando enviado: {command}, Resposta: {response}')
                return response
        except SerialException as e:
            logger.error(f'Falha ao enviar comando {command}: {e}')
            return ''

    def send_commands(self, commands:[str]) -> [str]:
        status = self.status()
        if status:
            logger.error(f'Erro {status} ao enviar comandos')
            return []

        out_list = []
        for cmd in commands:
            out = self.send_command(cmd)
            if out:
                out_list.append(out)

        return out_list if len(out_list) else [] 

    def read_response(self) -> str:
        status = self.status()
        if status:
            logger.error(f'Erro {status} ao ler resposta')
            return ''

        response = self.ser.readline().decode()
        self.ser.flush()
        logger.debug(f'Resposta lida: {response}')
        return response

    def device_id(self):
        res = self.send_command('ID?')        
        if res:
            res = res.strip().split(',')
            device_info = {
                "Model": res[0],
                "Serial Number": res[1],
                "Firmware Version": res[2]   
            }
            logger.info(f'Informações do dispositivo: {device_info}')
            return device_info
        logger.warning('Falha ao obter informações do dispositivo')
        return None 

    def ch1_freq(self):
        CH1_FREQ = [
            "MEASU:IMM:SOURCE CH1",
            "MEASU:IMM:TYPE FREQ",
            "MEASU:IMM:VAL?"
        ]
        logger.info('Obtendo frequência do canal 1')
        res = self.send_commands(CH1_FREQ)
        if res:
            return res[0]
        return None

    def ch2_freq(self):
        CH2_FREQ = [
            "MEASU:IMM:SOURCE CH2",
            "MEASU:IMM:TYPE FREQ",
            "MEASU:IMM:VAL?"
        ]
        logger.info('Obtendo frequência do canal 2')
        res =  self.send_commands(CH2_FREQ)
        if res:
            return res[0]
        return None    


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
        logger.info('Obtendo waveform do canal 1')
        res = self.send_commands(CH1_WAVEFORM)
        if res:
            return Waveform(res[0], res[1]) 
        logger.warning('Falha ao obter waveform do canal 1')
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
        logger.info('Obtendo waveform do canal 2')
        res = self.send_commands(CH2_WAVEFORM)
        if res:
            return Waveform(res[0], res[1])
        logger.warning('Falha ao obter waveform do canal 2')
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
        logger.info('Obtendo waveform matemática')
        res = self.send_commands(MATH_WAVEFORM)
        if res:
            return Waveform(res[0], res[1])
        logger.warning('Falha ao obter waveform matemática')
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
        logger.info('Obtendo waveform de referência 1')
        res = self.send_commands(REF1_WAVEFORM)
        if res:
            return Waveform(res[0], res[1])
        logger.warning('Falha ao obter waveform de referência 1')
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
        logger.info('Obtendo waveform de referência 2')
        res = self.send_commands(REF2_WAVEFORM)
        if res:
            return Waveform(res[0], res[1])
        logger.warning('Falha ao obter waveform de referência 2')
        return None

    def event_log(self):
        EVENT_LOG = [
            "*ESR?",
            "ALLE?"
        ]
        logger.info('Obtendo logs de eventos')
        return self.send_commands(EVENT_LOG)


if __name__ == '__main__':
    tek = Tektronix()
    tek.start()
        
    waveform = tek.ch1_waveform()
    #waveform = Waveform.build_waveform_by_txt('2025-02-11_15:20:28_199721.txt')

    print(waveform)
    
    if waveform:
        WaveformPlot(waveform).plot()        
        #plot_xy(x, y, y_min, y_max)
        #waveform.generate_csv()
        #waveform.generate_waveform_txt()  
    
    pass