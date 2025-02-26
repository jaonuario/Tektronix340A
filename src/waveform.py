import csv
import datetime
import os
import io
import matplotlib.pyplot as plt
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Waveform:
    def __init__(self, wfmpr_response: str, curv_response: str = None, output_dir='waveform_data'):
        """
        Inicializa a classe com a resposta do comando WFMPR? e CURV?.
        
        Parâmetros:
            wfmpr_response (str): Resposta bruta do comando WFMPR?.
            curv_response (str, opcional): Resposta bruta do comando CURV?.
            output_dir (str, opcional): Diretório padrão para salvar arquivos.
        """
        self.raw_data = wfmpr_response
        self.curv_data = curv_response
        self.parsed_data = self._parse_response()
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        logging.info(f"Waveform inicializada com sucesso. Diretório de saída: {self.output_dir}")
    
    def _parse_response(self):
        """
        Processa a resposta do WFMPR? e retorna um dicionário com os parâmetros nomeados.
        """
        values = self.raw_data.split(';')
        parsed_data = {
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
        logging.info("Resposta do WFMPR? processada com sucesso.")
        return parsed_data
    
    def get_data(self):
        """Retorna os dados processados."""
        logging.info("Dados processados retornados.")
        return self.parsed_data
    
    def get_waveform_data(self)->dict[str:str]:
        """Retorna as informações da waveform"""
        data = self.parsed_data["WAVEFORM_INFO"].split(',')
        waveform_data = {
            "CHANNEL": data[0],
            "COUPLING": data[1],
            "VOLTAGE_PER_DIVISION": data[2],
            "TIME_PER_DIVISION": data[3],
            "POINTS": data[4],
            "MODE": data[5]
        }
        logging.info("Informações da waveform retornadas.")
        return waveform_data

    def get_raw_curv_data(self):
        """Retorna os dados brutos de CURV? como um array de inteiros."""
        if not self.curv_data:
            logging.warning("Nenhum dado CURV? disponível.")
            return None
        logging.info("Dados brutos de CURV? retornados.")
        return list(map(int, self.curv_data.split(',')))

    def process_curv_data(self):
        """Processa os valores de CURV? e retorna uma lista de tensões convertidas."""
        if not self.curv_data:
            logging.warning("Nenhum dado CURV? disponível para processamento.")
            return None
        
        data_points = list(map(int, self.curv_data.split(',')))
        y_increment = self.parsed_data["YINCREMENT"]
        y_zero = self.parsed_data["YZERO"]

        processed_data = [y_zero + (y_increment * point) for point in data_points]
        logging.info("Dados CURV? processados com sucesso.")
        return processed_data

    def get_time_array(self):
        """Retorna um array de tempo correspondente aos pontos da forma de onda."""
        num_points = self.parsed_data["NUM_POINTS"]
        x_increment = self.parsed_data["XINCREMENT"]
        x_zero = self.parsed_data["XZERO"]
        
        time_array = [x_zero + i * x_increment for i in range(num_points)]
        logging.info("Array de tempo gerado com sucesso.")
        return time_array

    def get_voltage_max(self):
        """Retorna o limite superior dos valores de CURV? convertidos em tensão."""
        bit_depth = self.parsed_data["BIT_DEPTH"]
        max_value = (2 ** (bit_depth - 1)) - 1  # Assumindo valores com sinal
        voltage_max = self.parsed_data["YZERO"] + (self.parsed_data["YINCREMENT"] * max_value)
        logging.info(f"Limite superior de tensão calculado: {voltage_max} V")
        return voltage_max
    
    def get_voltage_min(self):
        """Retorna o limite inferior dos valores de CURV? convertidos em tensão."""
        bit_depth = self.parsed_data["BIT_DEPTH"]
        min_value = -(2 ** (bit_depth - 1))  # Assumindo valores com sinal
        voltage_min = self.parsed_data["YZERO"] + (self.parsed_data["YINCREMENT"] * min_value)
        logging.info(f"Limite inferior de tensão calculado: {voltage_min} V")
        return voltage_min

    def save_to_file(self, file_format='txt', name: str | None = None, output_dir: str | None = None):
        """
        Salva os dados brutos de WFMPR? e CURV? em um arquivo .txt ou .csv.
        
        Parâmetros:
            name (str, opcional): Nome do arquivo. Se não for fornecido, usa a data e hora atual.
            file_format (str, opcional): Formato do arquivo ('txt' ou 'csv'). Padrão é 'txt'.
            output_dir (str, opcional): Diretório onde o arquivo será salvo. Se não for fornecido, usa o diretório padrão.
        """
        if not name:
            name = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Define o diretório de saída
        save_dir = output_dir if output_dir is not None else self.output_dir
        
        # Cria o caminho completo do arquivo
        file_path = os.path.join(save_dir, f"{name}.{file_format}")
        
        # Garante que o diretório de saída exista
        os.makedirs(save_dir, exist_ok=True)
        
        if file_format == 'txt':
            with open(file_path, 'w') as file:
                file.write(self.raw_data + '\n')
                if self.curv_data:
                    file.write(self.curv_data + '\n')
            logging.info(f"Dados salvos em {file_path} no formato TXT.")
        elif file_format == 'csv':
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["WFMPR Data", self.raw_data])
                if self.curv_data:
                    writer.writerow(["CURV Data", self.curv_data])
            logging.info(f"Dados salvos em {file_path} no formato CSV.")
        else:
            logging.error("Formato de arquivo inválido. Use 'txt' ou 'csv'.")
            raise ValueError("Formato de arquivo inválido. Use 'txt' ou 'csv'.")
    
    @staticmethod
    def from_file(file_name: str):
        """
        Cria uma instância da classe Waveform a partir de um arquivo .txt ou .csv.
        
        Parâmetros:
            file_name (str): Nome do arquivo (.txt ou .csv).
        """
        if not (file_name.endswith('.txt') or file_name.endswith('.csv')):
            logging.error("Tipo de arquivo inválido. Use .txt ou .csv.")
            raise ValueError("Tipo de arquivo inválido. Use .txt ou .csv.")
        
        try:
            with open(file_name, 'r') as file:
                if file_name.endswith('.txt'):
                    header = file.readline().strip()
                    curv = file.readline().strip()
                elif file_name.endswith('.csv'):
                    reader = csv.reader(file)
                    header = next(reader)[1]
                    curv = next(reader)[1] if next(reader, None) else None
                logging.info(f"Waveform criada a partir do arquivo {file_name}.")
                return Waveform(header, curv if curv else None)
        except FileNotFoundError:
            logging.error(f"Arquivo não encontrado: {file_name}")
            raise FileNotFoundError("Arquivo não encontrado.")

    def __str__(self):
        """
        Retorna uma representação formatada dos dados processados.
        """
        return "\n".join(f"{key}: {value}" for key, value in self.parsed_data.items())


class WaveformPlot:
    def __init__(self, waveform:Waveform):
        """
        Inicializa a classe com um objeto Waveform.
        
        Parâmetros:
            waveform (Waveform): Objeto Waveform contendo os dados da forma de onda.
        """
        self.waveform = waveform
        self.figure, self.ax = plt.subplots()  # Cria uma figura e um eixo para o gráfico
        logging.info("WaveformPlot inicializado com sucesso.")

    def _plot_config(self):
        """
        Configura os rótulos dos eixos, título, legenda, grid e limites de y.
        """
        # Configurações básicas do gráfico
        self.ax.set_xlabel('Time (s)')
        self.ax.set_ylabel('Voltage (V)')
        self.ax.set_title('Waveform Plot com Limites de Y')
        self.ax.legend()
        self.ax.grid(True)

        # Define os limites de y
        y_upper_limit = self.waveform.get_voltage_max()
        y_lower_limit = self.waveform.get_voltage_min()

        # Define os limites no gráfico
        if y_lower_limit is not None and y_upper_limit is not None:
            self.ax.set_ylim(y_lower_limit, y_upper_limit)
        logging.info("Configurações do gráfico aplicadas.")

    def plot(self):
        """
        Plota a forma de onda no gráfico com limites de y.
        """
        # Obtém os dados de tempo e tensão
        x = self.waveform.get_time_array()
        y = self.waveform.process_curv_data()
        
        if x and y:
            # Plota a forma de onda
            self.ax.plot(x, y, label='Waveform', color='blue')
            
            # Configura o gráfico com limites de y
            self._plot_config()
            
            # Exibe o gráfico
            plt.show()
            logging.info("Gráfico da forma de onda exibido com sucesso.")
        else:
            logging.warning("Dados insuficientes para plotar a forma de onda.")

    def get_bitmap(self):
        """
        Retorna o gráfico da forma de onda como um bitmap (array de bytes).
        
        Retorna:
            bytes: Bitmap da forma de onda.
        """
        # Obtém os dados de tempo e tensão
        x = self.waveform.get_time_array()
        y = self.waveform.process_curv_data()
        
        if x and y:
            # Plota a forma de onda
            self.ax.plot(x, y, label='Waveform', color='blue')
            
            # Configura o gráfico com limites de y
            self._plot_config()
            
            # Cria um buffer de memória para salvar o gráfico
            buffer = io.BytesIO()
            self.figure.savefig(buffer, format='jpeg')
            buffer.seek(0)  # Volta ao início do buffer
            
            # Retorna os bytes do bitmap
            logging.info("Bitmap da forma de onda gerado com sucesso.")
            return buffer.getvalue()
        
        logging.warning("Dados insuficientes para gerar o bitmap.")
        return None

    def save_bitmap(self, name:str|None=None):
        """
        Salva o gráfico da forma de onda em um arquivo BMP.
        
        Parâmetros:
            name (str, opcional): Nome do arquivo BMP. Se None, usa um nome padrão.
        """
        if not name:
            name = "waveform_plot.bmp"
        
        # Obtém os dados de tempo e tensão
        x = self.waveform.get_time_array()
        y = self.waveform.process_curv_data()
        
        if x and y:
            # Plota a forma de onda
            self.ax.plot(x, y, label='Waveform', color='blue')
            
            # Configura o gráfico com limites de y
            self._plot_config()
            
            # Salva o gráfico em um arquivo BMP
            self.figure.savefig(name, format='jpeg')
            plt.close(self.figure)
            logging.info(f"Gráfico salvo como {name}.")
        else:
            logging.warning("Dados insuficientes para salvar o gráfico.")


if __name__ == '__main__':
    try:
        # Carrega a forma de onda a partir de um arquivo TXT
        waveform = Waveform.from_file('2025-02-11_15:48:57_142614.txt')
        print(waveform)
        
        if waveform:
            print(waveform.get_waveform_data())
            waveform.save_to_file()
            # Cria o plotter
            plotter = WaveformPlot(waveform)
            
            # Plota a forma de onda com limites automáticos
            plotter.plot()
            
            # Plota a forma de onda com limites personalizados
            plotter.plot()
            
            # Salva o gráfico em BMP com limites automáticos
            plotter.save_bitmap("waveform_auto_limits.bmp")
            
            # Salva o gráfico em BMP com limites personalizados
            plotter.save_bitmap("waveform_custom_limits.bmp")
            
            # Obtém o bitmap da forma de onda com limites automáticos
            bitmap = plotter.get_bitmap()
            if bitmap:
                print(f"Bitmap gerado com {len(bitmap)} bytes.")
            else:
                print("Erro ao gerar bitmap.")

    except Exception as e:
        print(f"Erro: {e}")