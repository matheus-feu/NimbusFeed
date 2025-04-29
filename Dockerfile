# Use a imagem oficial do Python runtime como imagem base
FROM python:3.12

MAINTAINER Matheus Feu <matheusfeu@gmail.com>

# Defina o diretório de trabalho
WORKDIR /app

 Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Atualize os pacotes e instale as dependências
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    libnss3 \
    lsb-release \
    xdg-utils \
    google-chrome-stable

# Install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/ curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Atualizar o pip
RUN pip install --upgrade pip

# Copie o arquivo de requisitos para o diretório de trabalho atual
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código-fonte para o diretório de trabalho atual
COPY . .

# Exponha a variável de ambiente para que as saídas sejam exibidas no log do Docker
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# Execute o aplicativo quando o contêiner for iniciado
CMD ["python", "run.py", "--selenoid-uri", "http://selenoid:4444"]