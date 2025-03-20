import time
import logging
from serial import Serial, EIGHTBITS, STOPBITS_ONE, PARITY_NONE, SerialException
from serial.tools import list_ports
from .waveform import Waveform, WaveformPlot

# Configuração do logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tektronix.log'),   # Log para arquivo
        logging.StreamHandler()                 # Log para o console
    ]
)
logger = logging.getLogger('Tektronix')

class Tektronix():
    def __init__(self, baudrate=19200, bytesize=EIGHTBITS, stopbits=STOPBITS_ONE):
        self.__ser = Serial(baudrate=baudrate, bytesize=bytesize, stopbits=stopbits, timeout=1)
        self.__find_device()

        self.device_info = None
        logger.info('Objeto Tektronix inicializado')

    def __find_device(self):
        for port in list_ports.comports():
            try:
                self.__ser.port = port.device
                self.__ser.open()
                self.__ser.write(b"ID?\n")
                response = self.__ser.readline().decode().strip()
                print(response)
                if "TEK/TDS 340A" in response.upper():
                    print(f"Osciloscópio encontrado em {port.device}: {response}")
                    return
                self.__ser.close()
            except Exception as e:
                print(f"Erro ao acessar {port.device}: {e}")
        raise Exception("Nenhum ociloscópio Tektronix foi encontrado")
    
    def __re_open_port(self):
        if self.__ser.isOpen():
            self.__ser.close()
        self.__ser.open()

    #TODO: sincronizar as propriedades do objeto com as configurações do dispositivo antes de aplicar
    @property
    def baudrate(self):
        return self.__ser.baudrate
    
    @baudrate.setter
    def baudrate(self, new_baudrate):
        self.__ser.baudrate = new_baudrate
        self.__re_open_port()

    @property
    def bytesize(self):
        return self.__ser.bytesize

    @bytesize.setter
    def bytesize(self, new_bytesize):
        self.__ser.bytesize = new_bytesize
        self.__re_open_port()

    @property
    def stopbits(self):
        return self.__ser.stopbits

    @stopbits.setter
    def stopbits(self, new_stopbits):
        self.__ser.stopbits = new_stopbits
        self.__re_open_port()

    #TODO: verificar a necessidade desses métodos
    @staticmethod
    def get_baudrate_list()->list[int]:
        logger.debug('Lista de baudrates solicitada')
        return [1200, 2400, 4800, 9600, 19200]
    
    @staticmethod
    def get_list_ports()->list[str]:
        logger.debug('Lista de portas seriais solicitada')
        return [port.device for port in list_ports.comports()]

    def close_port(self):
        if self.__ser.isOpen():
            self.__ser.close()
            logger.info('Porta serial fechada')

    def command(self, command:str) -> str:
        if not isinstance(command, str):
            raise TypeError("The command must be a str")

        if not self.__ser.is_open:
            raise TektronixError("Porta não disponível")

        try:
            self.__ser.write(command.encode() + b'\n')
            response = self.read_response().strip()

            self.__ser.write(b"*ESR?\n")
            error = self.__ser.readline().decode().strip()
            if error and error != "0":
                self.__ser.write(b"ALLE?")
                error_details = self.__ser.readline().decode().strip()
                raise TektronixError(f"Erro ao executar '{command}': ({error}) {error_details}")
            return response
            
        except SerialException as e:
            logger.error(f'Falha ao enviar comando {command}: {e}')
            return ''

    def commands(self, commands:list[str]) -> list[str]:
        out_list = []
        for cmd in commands:
            out = self.command(cmd)
            if out:
                out_list.append(out)
        return out_list

    def read_response(self) -> str:
        if not self.__ser.is_open:
            raise Exception("Porta não disponível")
        response = self.__ser.readline().decode()
        self.__ser.flush()
        logger.debug(f'Resposta lida: {response}')
        return response

    def device_id(self):
        res = self.command('ID?')
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
        res = self.commands(CH1_FREQ)
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
        res =  self.commands(CH2_FREQ)
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
        res = self.commands(CH1_WAVEFORM)
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
        res = self.commands(CH2_WAVEFORM)
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
        res = self.commands(MATH_WAVEFORM)
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
        res = self.commands(REF1_WAVEFORM)
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
        res = self.commands(REF2_WAVEFORM)
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
        return self.commands(EVENT_LOG)


class TektronixError(Exception):
    """ Exceção personalizada para erros do Tektronix. """
    pass