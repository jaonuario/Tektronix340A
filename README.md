# Tektronix340A

Este repositório contém um projeto para a criação de uma aplicação que permite a comunicação via interface serial entre um computador e um dispositivo Tektronix. Como se trata de um equipamento antigo, a única forma de extrair dados dele era originalmente por meio de disquetes (um objeto que as crianças de hoje provavelmente nem sabem que existiu). Por isso, surgiu a necessidade de desenvolver uma aplicação alternativa.

Foi instalada no aparelho uma placa de rede com comunicação RS232 para utilizar um software de terceiros. No entanto, esse software apresenta diversas limitações, como dificuldades de uso e falhas em aspectos essenciais da Interação Humano-Computador (IHC). Diante desses problemas, este projeto foi criado. Esta é a primeira versão da aplicação, que ainda contém diversos bugs e falta de testes, mas já é possível utilizá-la com cuidado.

Para iniciar o programa, utilize o seguinte comando (apenas em Linux):

```sh
sh initializer.sh
```

Caso utilize Windowns, execute em um terminal como administrador e não esqueça de adicionar o diretorio `./src` no path do python de busca de modulos. Vou ajeitar esse impecilho no futuro.

![image1](/screenshots/screenshot.png)

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

### Mensagens de Erro e Soluções

#### Erro: Dispositivo `/dev/ttyUSB0` não encontrado
- **Solução**: Certifique-se de que o dispositivo está conectado ao sistema.

#### Erro: Falha ao executar o script Python
- **Solução**: Verifique se o script `app.py` está corretamente configurado e se todos os módulos necessários estão disponíveis.

---
