#!/bin/bash

# Verifica se o dispositivo /dev/ttyUSB0 existe
if [ ! -e /dev/ttyUSB0 ]; then
  echo "Erro: O dispositivo /dev/ttyUSB0 não foi encontrado."
  echo "Certifique-se de que o dispositivo está conectado."
  exit 1
fi

# Tenta alterar as permissões do dispositivo
echo "Verificando permissões para /dev/ttyUSB0..."
if sudo chmod 666 /dev/ttyUSB0; then
  echo "Permissões alteradas com sucesso para /dev/ttyUSB0."
else
  echo "Erro: Não foi possível alterar as permissões de /dev/ttyUSB0."
  echo "Soluções possíveis:"
  echo "1. Execute o script com permissões de superusuário (sudo)."
  echo "2. Adicione seu usuário ao grupo 'dialout' com o comando:"
  echo "   sudo usermod -a -G dialout $USER"
  echo "3. Crie uma regra udev permanente para o dispositivo."
  exit 1
fi

# Configura o PYTHONPATH
echo "Configurando PYTHONPATH..."
export PYTHONPATH="${PYTHONPATH}:/home/donkey-slayer/repos/tektronix/src"
echo "PYTHONPATH atualizado: $PYTHONPATH"

# Executa o script Python
echo "Executando o script Python app.py..."
python3 app.py

# Verifica se o script Python foi executado com sucesso
if [ $? -eq 0 ]; then
  echo "Script Python app.py executado com sucesso!"
else
  echo "Erro: Falha ao executar o script Python app.py."
  exit 1
fi

exit 0