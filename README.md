# Candidate Processor API

Backend da aplicação **Candidate Processor**, desenvolvida como projeto de aprendizado para explorar a construção de uma API com Python/FastAPI e a integração entre diferentes serviços da AWS.

A aplicação recebe arquivos CSV contendo dados e notas de candidatos. O processamento é realizado de forma assíncrona e, ao final, os candidatos que atingiram a nota mínima são disponibilizados pela API.

## Arquitetura

O backend foi estruturado utilizando uma separação entre rotas, controllers, services, repositories, schemas e models.

```text
Frontend
   │
   │ POST /job
   ▼
FastAPI
   │
   ├── Cria Job
   │      │
   │      └── PostgreSQL / RDS
   │
   └── Gera Presigned URL
             │
             ▼
            S3
             │
             │ ObjectCreated
             ▼
            SQS
             │
             ▼
           Lambda
             │
             ├── Lê CSV do S3
             ├── Processa candidatos
             └── Persiste resultados
                    │
                    ▼
               PostgreSQL / RDS
```

## Fluxo de processamento

### 1. Criação do Job

O frontend envia apenas o nome do arquivo para:

```http
POST /job
```

A API cria um Job no banco de dados e gera uma chave para o arquivo no S3:

```text
jobs/{job_id}/input/{filename}
```

Em seguida, a API gera uma **Presigned URL** para upload do arquivo.

A API não recebe o arquivo diretamente.

### 2. Upload para o S3

A Presigned URL permite que o frontend faça o upload diretamente para o Amazon S3.

Isso evita que o arquivo precise passar pela API antes de chegar ao armazenamento.

> A implementação do upload e a integração do frontend com a Presigned URL estão documentadas no repositório do frontend.

### 3. Processamento assíncrono

Após o arquivo ser armazenado no S3, um evento de criação de objeto envia uma mensagem para uma fila Amazon SQS.

A fila desacopla o upload do processamento.

```text
S3
 │
 │ ObjectCreated
 ▼
SQS
 │
 ▼
Lambda
```

A Lambda então:

1. recebe a mensagem;
2. identifica o arquivo no S3;
3. baixa o CSV;
4. processa os candidatos;
5. persiste os resultados no PostgreSQL;
6. atualiza o Job.

### 4. Consulta do resultado

O frontend consulta o status do Job:

```http
GET /job/{job_id}
```

Após o processamento, os candidatos podem ser recuperados através de:

```http
GET /job/{job_id}/candidates
```

---

# Estrutura da aplicação

```text
candidate-processor-api/
│
├── app/
│   ├── aws/
│   │   └── s3.py
│   ├── config/
│   │   └── settings.py
│   ├── controllers/
│   │   ├── candidates.py
│   │   └── job.py
│   ├── database/
│   │   ├── engine.py
│   │   └── url.py
│   ├── dependencies/
│   │   ├── candidates.py
│   │   └── job.py
│   ├── models/
│   │   ├── base.py
│   │   ├── candidates.py
│   │   └── job.py
│   ├── repositories/
│   │   ├── candidates.py
│   │   └── job.py
│   ├── routes/
│   │   └── job.py
│   ├── schemas/
│   │   ├── candidates.py
│   │   └── job.py
│   ├── services/
│   │   └── job.py
│   └── main.py
│
├── alembic/
├── requirements.txt
└── run.py
```

### Responsabilidade das camadas

**Routes** — definem os endpoints HTTP e recebem as requisições.

**Controllers** — fazem a intermediação entre as rotas e a camada de serviço.

**Services** — concentram a lógica de negócio.

**Repositories** — responsáveis pelo acesso aos dados persistidos.

**Models** — representam as entidades do banco através do ORM.

**Schemas** — definem os modelos de entrada e saída utilizando Pydantic.

**AWS** — contém as integrações da aplicação com os serviços da AWS.

---

# AWS

## Amazon S3

Utilizado para armazenar os arquivos CSV enviados para processamento.

A API gera uma Presigned URL utilizando o AWS SDK (Boto3), permitindo que o cliente faça um upload `PUT` diretamente para o bucket.

A URL possui tempo de expiração e é associada a uma chave específica do Job.

## Amazon SQS

Utilizado como fila para desacoplar o upload do processamento.

Quando um novo arquivo é criado no S3, uma notificação é enviada para a fila.

Isso permite que o processamento aconteça de forma assíncrona.

## AWS Lambda

A Lambda é responsável pelo processamento dos arquivos recebidos através da fila.

Ela recupera o objeto armazenado no S3, processa os candidatos e persiste os resultados no banco de dados.

## Amazon RDS

Utilizado como banco de dados PostgreSQL para persistir:

- Jobs
- Candidatos
- Status do processamento
- Quantidade total de candidatos
- Quantidade de candidatos aprovados
- Datas de criação e conclusão

## Amazon EC2

Utilizado para hospedar a API FastAPI em produção.

## IAM

As permissões entre os serviços AWS são controladas através de IAM.

A Lambda, por exemplo, possui permissões específicas para acessar os recursos necessários durante o processamento.

---

# Endpoints

## Criar Job

```http
POST /job
```

### Request

```json
{
  "filename": "candidatos.csv"
}
```

### Response

```json
{
  "id": "uuid",
  "filename": "candidatos.csv",
  "upload_url": "https://..."
}
```

A resposta contém a Presigned URL utilizada pelo frontend para enviar o arquivo diretamente ao S3.

## Consultar Job

```http
GET /job/{job_id}
```

Exemplo:

```json
{
  "id": "uuid",
  "filename": "candidatos.csv",
  "status": "COMPLETED",
  "total_candidates": 100,
  "approved_candidates": 35,
  "created_at": "...",
  "completed_at": "..."
}
```

Estados possíveis:

```text
PENDING
PROCESSING
COMPLETED
FAILED
```

## Consultar candidatos

```http
GET /job/{job_id}/candidates
```

Retorna os candidatos associados ao Job.

---

# Tecnologias

### Backend

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- Boto3

### AWS

- Amazon S3
- Amazon SQS
- AWS Lambda
- Amazon RDS
- Amazon EC2
- IAM

### Infraestrutura

- Nginx
- HTTPS
- Route 53

---

# Configuração local

## Requisitos

- Python 3.14+
- PostgreSQL
- Conta AWS

## Instalação

```bash
git clone https://github.com/LuisG-santos/candidate-processor-api.git
cd candidate-processor-api

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Configure as variáveis de ambiente necessárias em um arquivo `.env`.

Execute as migrations:

```bash
alembic upgrade head
```

Inicie a aplicação:

```bash
python run.py
```

A API estará disponível em:

```text
http://localhost:8000
```

Documentação interativa:

```text
http://localhost:8000/docs
```

---

# Objetivo do projeto

Este projeto foi desenvolvido como uma experiência prática para estudar:

- Desenvolvimento de APIs com FastAPI
- Arquitetura em camadas
- Processamento assíncrono
- Message queues
- Presigned URLs
- Integração entre serviços AWS
- IAM e permissões
- Persistência com PostgreSQL
- Deploy de uma aplicação backend na AWS

O objetivo principal não é representar uma arquitetura de produção completa, mas explorar na prática como diferentes componentes de uma aplicação podem ser integrados utilizando serviços gerenciados da AWS.
