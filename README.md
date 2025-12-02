# DeméterAI

## Sobre o Projeto

Este é o repositório para o versionamento do projeto **DeméterAI**, um dashboard baseado em machine learning que executa a classificação e contagem de crisópideos utilizados como controle biológico de pragas em plantações.

O objetivo principal do projeto é automatizar e trazer precisão aos processos de contagem e classificação dos insetos, auxiliando produtores rurais e agrônomos na tomada de decisão para o controle de pragas de forma sustentável.

---

## Docker - Guia de Instalação e Execução

Este projeto utiliza **Docker Compose** para orquestrar múltiplos serviços como Backend, Frontend, Banco de Dados, Machine Learning e Ferramentas de Administração. Por isso, para o funcionamento adequado do projeto, é necessário utilizar o Docker Desktop.

### Pré-requisitos

Certifique-se de ter o **Docker** e o **Docker Compose** instalados em sua máquina.

[ [Instalar Docker](https://docs.docker.com/get-docker/ "null") ]

### 1. Clonar o Repositório

Clone o projeto para sua máquina local e acesse a pasta raiz:

```
git clone [https://github.com/MatthewF1331/DemeterAI.git](https://github.com/MatthewF1331/DemeterAI.git)
cd DemeterAI
```

### 2. Estrutura do Ambiente

O ambiente Docker está configurado para subir os seguintes serviços, definidos no `docker-compose.yml`:

* **db** `postgres` - Banco de dados em PostgreSQL.
* **backend** `fastapi` - API principal rodando na porta `8000`.
* **demeterai** `ml worker` - Código do Machine Learning para processamento.
* **frontend** `nginx` - Servidor web para os arquivos estáticos na porta `8080`.
* **pgadmin -** Interface para gerenciamento do banco de dados na porta `5050`.

### 3. Build e Execução

Como os arquivos de configuração `Dockerfile` e `docker-compose.yml` estão na raiz do projeto, é necessário acessar a raiz do arquivo para executá-los. Para isso, utilize o comando abaixo no **Terminal** do **Docker Desktop** (ou no seu terminal de preferência) para acessar o diretório:

```
cd <caminho do seu diretório>
```

Seu terminal deve estar direcionado para o diretório da seguinte forma (exemplo Windows): `PS C:\Users\Usuário\documents\github\demeterAI>`

Após isso, utilize o comando abaixo para construir as imagens e iniciar todos os containers simultaneamente:

```
docker compose up --build

```

*O parâmetro ********************************************************************************************************************************************************************************************************************************`--build`******************************************************************************************************************************************************************************************************************************** garante que as imagens do backend e do worker de ML sejam recriadas com as alterações mais recentes do código.*

Aguarde até que todos os serviços estejam iniciados.

### 4. Acessando os Serviços

Após o ambiente iniciar, você pode acessar as interfaces através das seguintes URLs:

| ServiçoURLDescrição |                         |                                |
| ------------------- | ----------------------- | ------------------------------ |
| **Frontend**        | `http://localhost:8080` | Interface do Dashboard (Nginx) |
| **pgAdmin**         | `http://localhost:5050` | Gerenciador do Banco de Dados  |

Ou você pode ir até a aba **Containers** do **Docker Desktop** e verificar na coluna **Port(s)** a porta do container que você deseja acessar.

**Credenciais Padrão (Ambiente de Desenvolvimento):**

**Postgres:** 

```
USER     = postgres
PASSWORD = 1234
DB       = demeter
```

**Pgadmin:** 

```
EMAIL    = admin@admin.com
PASSWORD = admin
```

## Comandos Úteis

Para parar a execução de todos os serviços e liberar os terminais:

```
docker compose down

```

Para rodar em segundo plano (modo "detached"):

```
docker compose up -d

```

Para visualizar os logs de um serviço específico (ex: backend):

```
docker compose logs -f backend

```

## Tecnologias Utilizadas

* **Linguagem:** Python, HTML, CSS, JavaScript.
* **Framework Backend:** FastAPI, Uvicorn, SQLAlchemy
* **Machine Learning:** Ultralytics (YOLOv8n), PyTorch, OpenCV, NumPy
* **Banco de Dados:** PostgreSQL 15
* **Frontend:** Nginx (Servindo arquivos estáticos)
* **Infraestrutura:** Docker e Docker Compose

## Agradecimentos

Agradecemos a empresa Predativa por nos fornecer a problemática do projeto, além do suporte para o desenvolvimento, e também a UNIPAM, por propiciar a oportunidade de projeto voltado ao desenvolvimento do mercado real.

## Referências

* **Documentação Ultralytics:** [https://docs.ultralytics.com/pt/models/yolov8/#what-are-the-performance-metrics-for-yolov8-models](https://www.google.com/search?q=https://docs.ultralytics.com/pt/models/yolov8/%23what-are-the-performance-metrics-for-yolov8-models "null")
* **Documentação Docker:** [https://docs.docker.com/compose/intro/compose-application-model/](https://docs.docker.com/compose/intro/compose-application-model/ "null")
