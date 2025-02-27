# Tektronix340A

Este repositório contém um projeto para a criação de uma aplicação que permite a comunicação via interface serial entre um computador e um dispositivo Tektronix. Como se trata de um equipamento antigo, a única forma de extrair dados dele era originalmente por meio de disquetes (um objeto que as crianças de hoje provavelmente nem sabem que existiu). Por isso, surgiu a necessidade de desenvolver uma aplicação alternativa.

Foi instalada no aparelho uma placa de rede com comunicação RS232 para utilizar um software de terceiros. No entanto, esse software apresenta diversas limitações, como dificuldades de uso e falhas em aspectos essenciais da Interação Humano-Computador (IHC). Diante desses problemas, este projeto foi criado. Esta é a primeira versão da aplicação, que ainda contém diversos bugs e falta de testes, mas já é possível utilizá-la com cuidado.

Para iniciar o programa, utilize o seguinte comando (apenas em Linux):

```sh
sh initializer.sh
```

Caso utilize Windowns, execute em um terminal como administrador e não esqueça de adicionar o diretorio `./src` no path do python de busca de modulos. Vou ajeitar esse impecilho no futuro.

![image1](/screenshots/screenshot.png)

A documentação a seguir foi gerada em sua totalidade por IA e ainda esta sendo revisada.

# Documentação

## Modulos utilízados

| Nome        | Versão    | Descrição                                                                   |
|-------------|-----------|-----------------------------------------------------------------------------|
| PySide6     | 6.8.1.1-3 | Biblioteca para criação de interfaces gráficas (GUI) usando o framework Qt. |
| pyqtgraph   | 0.13.7-2  | Biblioteca para visualização de gráficos e dados em tempo real.             |
| pyserial    | 3.5-7     | Biblioteca para comunicação serial com dispositivos (ex: Arduino, sensores).|


## Descrição do Arquivo `initializer.sh`

O arquivo `initializer.sh` é um script shell que prepara o ambiente para a execução de um script Python (`app.py`). Ele realiza as seguintes tarefas:

1. **Verifica a existência do dispositivo `/dev/ttyUSB0`**:
   - O script verifica se o dispositivo `/dev/ttyUSB0` está presente no sistema. Esse dispositivo é comumente usado para comunicação serial com dispositivos externos, como osciloscópios Tektronix.
   - Se o dispositivo não for encontrado, o script exibe uma mensagem de erro e encerra a execução.

2. **Altera as permissões do dispositivo `/dev/ttyUSB0`**:
   - O script tenta alterar as permissões do dispositivo para `666` (leitura e escrita para todos os usuários) usando o comando `sudo chmod`.
   - Se a alteração de permissões falhar, o script sugere soluções, como executar o script com `sudo`, adicionar o usuário ao grupo `dialout` ou criar uma regra `udev` permanente.

3. **Configura o `PYTHONPATH`**:
   - O script adiciona o diretório `/home/donkey-slayer/repos/tektronix/src` ao `PYTHONPATH`, permitindo que o Python importe módulos desse diretório.
   - O `PYTHONPATH` é uma variável de ambiente que define os diretórios onde o Python procura por módulos.

4. **Executa o script Python `app.py`**:
   - O script executa o arquivo `app.py` usando o comando `python3`.
   - Após a execução, ele verifica se o script Python foi concluído com sucesso. Se houver algum erro, o script exibe uma mensagem de erro e encerra a execução.

5. **Finalização**:
   - O script encerra com um código de status `0` em caso de sucesso ou `1` em caso de falha.

---

### Passos do Script

1. **Verificação do dispositivo `/dev/ttyUSB0`**:
   - Se o dispositivo não existir, o script exibe uma mensagem de erro e encerra.

2. **Alteração de permissões**:
   - Tenta alterar as permissões do dispositivo. Se falhar, sugere soluções e encerra.

3. **Configuração do `PYTHONPATH`**:
   - Adiciona o diretório especificado ao `PYTHONPATH`.

4. **Execução do script Python**:
   - Executa o script `app.py` e verifica se foi bem-sucedido.

5. **Finalização**:
   - Encerra o script com um código de status apropriado.

---

### Mensagens de Erro e Soluções

#### Erro: Dispositivo `/dev/ttyUSB0` não encontrado
- **Solução**: Certifique-se de que o dispositivo está conectado ao sistema.

#### Erro: Falha ao executar o script Python
- **Solução**: Verifique se o script `app.py` está corretamente configurado e se todos os módulos necessários estão disponíveis.

---

## Classe `Tektronix`

A classe `Tektronix` é responsável por gerenciar a comunicação com dispositivos Tektronix via porta serial. Ela permite a leitura de dados de waveform, frequência e logs de eventos, além de fornecer funcionalidades para plotagem e exportação de dados. A classe utiliza a biblioteca `pyserial` para comunicação serial e integra-se com um módulo `waveform` para processamento e visualização de dados.

---

### Métodos da Classe

Abaixo está uma tabela com todos os métodos da classe `Tektronix` e suas descrições:

| Método               | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `get_baudrate_list`  | Retorna uma lista de baudrates suportados.                                |
| `get_list_ports`     | Retorna uma lista de portas seriais disponíveis.                          |
| `status`             | Verifica o status da conexão serial.                                      |
| `start`              | Inicializa a conexão serial com o dispositivo.                           |
| `close_port`         | Fecha a porta serial.                                                    |
| `send_command`       | Envia um comando para o dispositivo e retorna a resposta.                |
| `send_commands`      | Envia uma lista de comandos e retorna uma lista de respostas.            |
| `read_response`      | Lê a resposta do dispositivo.                                            |
| `device_id`          | Obtém as informações do dispositivo (modelo, número de série, firmware). |
| `ch1_freq`           | Obtém a frequência do canal 1.                                           |
| `ch2_freq`           | Obtém a frequência do canal 2.                                           |
| `ch1_waveform`       | Obtém a waveform do canal 1.                                             |
| `ch2_waveform`       | Obtém a waveform do canal 2.                                             |
| `math_waveform`      | Obtém a waveform matemática.                                             |
| `ref1_waveform`      | Obtém a waveform de referência 1.                                        |
| `ref2_waveform`      | Obtém a waveform de referência 2.                                        |
| `event_log`          | Obtém logs de eventos do dispositivo.                                    |

---

### Detalhamento dos Métodos

#### `get_baudrate_list()`
- **Descrição**: Retorna uma lista de baudrates suportados para comunicação serial.
- **Argumentos**: Nenhum.
- **Retorno**: Lista de inteiros (`List[int]`).

---

#### `get_list_ports()`
- **Descrição**: Retorna uma lista de portas seriais disponíveis no sistema.
- **Argumentos**: Nenhum.
- **Retorno**: Lista de strings (`List[str]`).

---

#### `status()`
- **Descrição**: Verifica o status da conexão serial.
  - Retorna `0` se a conexão estiver OK.
  - Retorna `1` se a porta serial não estiver aberta.
  - Retorna `2` se a porta serial não estiver inicializada.
- **Argumentos**: Nenhum.
- **Retorno**: Inteiro (`int`).

---

#### `start()`
- **Descrição**: Inicializa a conexão serial com o dispositivo.
- **Argumentos**: Nenhum.
- **Retorno**: Inteiro (`int`). Retorna `1` em caso de sucesso e `0` em caso de falha.

---

#### `close_port()`
- **Descrição**: Fecha a porta serial.
- **Argumentos**: Nenhum.
- **Retorno**: Nenhum (`None`).

---

#### `send_command(command: str)`
- **Descrição**: Envia um comando para o dispositivo e retorna a resposta.
- **Argumentos**:
  - `command` (str): Comando a ser enviado.
- **Retorno**: String (`str`) com a resposta do dispositivo.

---

#### `send_commands(commands: List[str])`
- **Descrição**: Envia uma lista de comandos e retorna uma lista de respostas.
- **Argumentos**:
  - `commands` (List[str]): Lista de comandos a serem enviados.
- **Retorno**: Lista de strings (`List[str]`) com as respostas.

---

#### `read_response()`
- **Descrição**: Lê a resposta do dispositivo.
- **Argumentos**: Nenhum.
- **Retorno**: String (`str`) com a resposta.

---

#### `device_id()`
- **Descrição**: Obtém as informações do dispositivo (modelo, número de série e versão do firmware).
- **Argumentos**: Nenhum.
- **Retorno**: Dicionário (`Dict[str, str]`) com as informações.

---

#### `ch1_freq()`
- **Descrição**: Obtém a frequência do canal 1.
- **Argumentos**: Nenhum.
- **Retorno**: String (`str`) com a frequência.

---

#### `ch2_freq()`
- **Descrição**: Obtém a frequência do canal 2.
- **Argumentos**: Nenhum.
- **Retorno**: String (`str`) com a frequência.

---

#### `ch1_waveform()`
- **Descrição**: Obtém a waveform do canal 1.
- **Argumentos**: Nenhum.
- **Retorno**: Objeto `Waveform`.

---

#### `ch2_waveform()`
- **Descrição**: Obtém a waveform do canal 2.
- **Argumentos**: Nenhum.
- **Retorno**: Objeto `Waveform`.

---

#### `math_waveform()`
- **Descrição**: Obtém a waveform matemática.
- **Argumentos**: Nenhum.
- **Retorno**: Objeto `Waveform`.

---

#### `ref1_waveform()`
- **Descrição**: Obtém a waveform de referência 1.
- **Argumentos**: Nenhum.
- **Retorno**: Objeto `Waveform`.

---

#### `ref2_waveform()`
- **Descrição**: Obtém a waveform de referência 2.
- **Argumentos**: Nenhum.
- **Retorno**: Objeto `Waveform`.

---

#### `event_log()`
- **Descrição**: Obtém logs de eventos do dispositivo.
- **Argumentos**: Nenhum.
- **Retorno**: Lista de strings (`List[str]`).

---

## Classe `Waveform`

A classe `Waveform` é responsável por processar e manipular dados de formas de onda obtidos de dispositivos Tektronix. Ela permite a leitura, processamento, visualização e exportação de dados de waveform, além de fornecer funcionalidades para plotagem e geração de gráficos.

---

### Métodos da Classe

Abaixo está uma tabela com todos os métodos da classe `Waveform` e suas descrições:

| Método               | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `_parse_response`    | Processa a resposta do comando `WFMPR?` e retorna um dicionário com os parâmetros. |
| `get_data`           | Retorna os dados processados da waveform.                                 |
| `get_waveform_data`  | Retorna as informações detalhadas da waveform.                            |
| `get_raw_curv_data`  | Retorna os dados brutos do comando `CURV?`.                               |
| `process_curv_data`  | Processa os valores de `CURV?` e retorna uma lista de tensões convertidas.|
| `get_time_array`     | Retorna um array de tempo correspondente aos pontos da forma de onda.     |
| `get_voltage_max`    | Retorna o limite superior dos valores de tensão.                          |
| `get_voltage_min`    | Retorna o limite inferior dos valores de tensão.                          |
| `save_to_file`       | Salva os dados brutos em um arquivo TXT ou CSV.                           |
| `from_file`          | Cria uma instância da classe a partir de um arquivo TXT ou CSV.           |
| `__str__`            | Retorna uma representação formatada dos dados processados.                |

---

### Detalhamento dos Métodos

#### `_parse_response()`
- **Descrição**: Processa a resposta do comando `WFMPR?` e retorna um dicionário com os parâmetros nomeados.
- **Argumentos**: Nenhum.
- **Retorno**: Dicionário (`Dict[str, Any]`) com os dados processados.

---

#### `get_data()`
- **Descrição**: Retorna os dados processados da waveform.
- **Argumentos**: Nenhum.
- **Retorno**: Dicionário (`Dict[str, Any]`) com os dados processados.

---

#### `get_waveform_data()`
- **Descrição**: Retorna as informações detalhadas da waveform, como canal, acoplamento, volts/divisão, etc.
- **Argumentos**: Nenhum.
- **Retorno**: Dicionário (`Dict[str, str]`) com as informações da waveform.

---

#### `get_raw_curv_data()`
- **Descrição**: Retorna os dados brutos do comando `CURV?` como um array de inteiros.
- **Argumentos**: Nenhum.
- **Retorno**: Lista de inteiros (`List[int]`) ou `None` se não houver dados.

---

#### `process_curv_data()`
- **Descrição**: Processa os valores de `CURV?` e retorna uma lista de tensões convertidas.
- **Argumentos**: Nenhum.
- **Retorno**: Lista de floats (`List[float]`) ou `None` se não houver dados.

---

#### `get_time_array()`
- **Descrição**: Retorna um array de tempo correspondente aos pontos da forma de onda.
- **Argumentos**: Nenhum.
- **Retorno**: Lista de floats (`List[float]`).

---

#### `get_voltage_max()`
- **Descrição**: Retorna o limite superior dos valores de tensão.
- **Argumentos**: Nenhum.
- **Retorno**: Float (`float`).

---

#### `get_voltage_min()`
- **Descrição**: Retorna o limite inferior dos valores de tensão.
- **Argumentos**: Nenhum.
- **Retorno**: Float (`float`).

---

#### `save_to_file(file_format='txt', name=None, output_dir=None)`
- **Descrição**: Salva os dados brutos de `WFMPR?` e `CURV?` em um arquivo TXT ou CSV.
- **Argumentos**:
  - `file_format` (str): Formato do arquivo (`'txt'` ou `'csv'`).
  - `name` (str, opcional): Nome do arquivo. Se não for fornecido, usa a data e hora atual.
  - `output_dir` (str, opcional): Diretório onde o arquivo será salvo.
- **Retorno**: Nenhum.

---

#### `from_file(file_name)`
- **Descrição**: Cria uma instância da classe `Waveform` a partir de um arquivo TXT ou CSV.
- **Argumentos**:
  - `file_name` (str): Nome do arquivo.
- **Retorno**: Instância da classe `Waveform`.

---

#### `__str__()`
- **Descrição**: Retorna uma representação formatada dos dados processados.
- **Argumentos**: Nenhum.
- **Retorno**: String (`str`).

---

## Classe `WaveformPlot`

A classe `WaveformPlot` é responsável por plotar e visualizar os dados de uma forma de onda. Ela utiliza a biblioteca `matplotlib` para gerar gráficos e permite a exportação de gráficos em formato de bitmap.

---

### Métodos da Classe

Abaixo está uma tabela com todos os métodos da classe `WaveformPlot` e suas descrições:

| Método               | Descrição                                                                 |
|----------------------|---------------------------------------------------------------------------|
| `_plot_config`       | Configura os rótulos dos eixos, título, legenda e grid do gráfico.        |
| `plot`               | Plota a forma de onda no gráfico com limites de tensão.                   |
| `get_bitmap`         | Retorna o gráfico da forma de onda como um bitmap (array de bytes).       |
| `save_bitmap`        | Salva o gráfico da forma de onda em um arquivo BMP.                       |

---

### Detalhamento dos Métodos

#### `_plot_config()`
- **Descrição**: Configura os rótulos dos eixos, título, legenda e grid do gráfico.
- **Argumentos**: Nenhum.
- **Retorno**: Nenhum.

---

#### `plot()`
- **Descrição**: Plota a forma de onda no gráfico com limites de tensão.
- **Argumentos**: Nenhum.
- **Retorno**: Nenhum.

---

#### `get_bitmap()`
- **Descrição**: Retorna o gráfico da forma de onda como um bitmap (array de bytes).
- **Argumentos**: Nenhum.
- **Retorno**: Bytes (`bytes`) ou `None` se não houver dados.

---

#### `save_bitmap(name=None)`
- **Descrição**: Salva o gráfico da forma de onda em um arquivo BMP.
- **Argumentos**:
  - `name` (str, opcional): Nome do arquivo BMP. Se não for fornecido, usa um nome padrão.
- **Retorno**: Nenhum.

---