# NimbusFeed

O NimbusFeed é um sistema de coleta e disponibilização de dados meteorológicos que combina web scraping e integração com
APIs de previsão do tempo.

## 📋 Pré-requisitos

- Python 3.13
- Docker
- virtualenv

## 🚀 Instalação

### Usando Python e virtualenv

1. Clone o repositório:
    ```bash
    git clone https://github.com/matheus-feu/NimbusFeed.git
   ``` 

2. Crie um ambiente virtual:
    ```bash
    cd NimbusFeed
    python -m venv venv
    source venv/bin/activate  # Linux/Mac
    venv\Scripts\activate  # Windows
    ```

3. Instale as dependências:
    ```bash
   pip install -r requirements.txt
   ```

### Usando Docker

1. Construa e inicie os containers:
    ```bash
    docker-compose up -d
    ```

## ⚙️ Configuração

### Variáveis de Ambiente

O projeto requer as seguintes variáveis de ambiente no arquivo `.env`:

### 📝 Notas importantes sobre as variáveis:

1. **USE_HEADLESS**
    - Recomendado manter `True` em produção para economia de recursos
    - Use `False` apenas durante desenvolvimento para debug visual

2. **USE_SELENOID**
    - Necessário `True` quando usando a infraestrutura do Selenoid
    - Configure `False` para desenvolvimento local com WebDriver

3. **API_KEY**
    - Obrigatória para consultas ao OpenWeatherMap
    - Registre-se gratuitamente em https://openweathermap.org/
    - Mantenha esta chave em segurança

4. **NAME_APP**
    - Identificador único da aplicação no Selenoid
    - Usado para rastreamento e logs
    - Evite caracteres especiais e espaços

5. **HOST e PORT**
    - Em ambiente local: geralmente `localhost:4444`
    - Com Docker: use o nome do serviço definido no docker-compose
    - Verifique se a porta não está em uso por outros serviços

## 🏃 Executando o Projeto

### Método Local

1. Ative o ambiente virtual (se ainda não estiver ativo)
2. Execute o servidor:
    ```bash
    python run.py
    ```
   Nesse momento o Selenoid ja está rodando após a do `docker-compose up -d`


3. Acesse a aplicação em `http://localhost:8000/docs`
![image](https://github.com/user-attachments/assets/59ed4dde-7614-4ac8-a154-e3e2f24d9723)

## 📁 Estrutura do Projeto

- Endpoints da API REST `/api`
- `/config` - Arquivos de configuração
- `/libs` - Bibliotecas auxiliares
- `/reports` - Relatórios gerados
- `/scraping` - Scripts de web scraping
- Ponto de entrada da aplicação `run.py`

## 🛠️ Funcionalidades Principais

1. **Consulta de Previsão do Tempo**
    - Endpoint: `/api/firecast`
    - Método: GET
    - Retorna dados meteorológicos atualizados apatir do scraping no site ClimaTempo

2. **Geração de Relatórios**
    - Endpoint: `/api/report/weather_forecast/csv`
    - Método: GET
    - Gera relatórios em CSV com dados meteorológicos

## 📦 Tecnologias Utilizadas

- Python
- SQLAlchemy
- Selenium
- Selenoid
- FastAPI
- Requests
- Docker

## 📝 Notas Adicionais

- O banco de dados `SQLite()` é criado automaticamente na primeira execução `nimbusfeed.db` ou o nome que escolher.
- O modo headless do Selenium pode ser configurado através da variável `USE_HEADLESS`
- Os relatórios gerados são obtidos através dos endpoints após requistar e realizar o download.
  `
