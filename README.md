# Candidate Processor API

Uma API robusta para processamento e gerenciamento de candidatos em processos de recrutamento. Desenvolvida com **FastAPI**, integrada com **AWS** (S3 e SQS) e utilizando **PostgreSQL** para persistência de dados.

## 🚀 Características

- ✅ **API RESTful** completa para gestão de vagas e candidatos
- ✅ **Integração AWS S3** para armazenamento de documentos
- ✅ **Fila de Processamento (SQS)** para processamento assíncrono
- ✅ **PostgreSQL** como banco de dados
- ✅ **CORS** configurado para aplicações frontend
- ✅ **Migrations** com Alembic
- ✅ **Type Hints** com Pydantic para validação de dados
- ✅ **UUID** para identificadores únicos

## 📋 Pré-requisitos

- Python 3.9+
- PostgreSQL 13+
- AWS Account (para SQS e S3)
- pip ou poetry

## 🔧 Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/LuisG-santos/candidate-processor-api.git
cd candidate-processor-api
```

### 2. Crie um ambiente virtual

```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Database
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=postgres
DATABASE_PASSWORD=sua_senha
DATABASE_NAME=candidate_processor

# AWS
AWS_PROFILE=default
AWS_REGION=us-east-1
BUCKET_NAME=seu-bucket-name

# Frontend
FRONT_URL=http://localhost:5173
```

### 5. Execute as migrations

```bash
alembic upgrade head
```

### 6. Inicie o servidor

```bash
python run.py
```

A API estará disponível em: **http://localhost:8000**

## 📚 Documentação da API

Após iniciar o servidor, acesse a documentação interativa:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔌 Endpoints Principais

### Jobs (Vagas)

#### Criar uma nova vaga
```http
POST /job
Content-Type: application/json

{
  "filename": "job_123.csv"
}
```

**Response (201)**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "job_123.csv",
  "status": "PENDING",
  "total_candidates": 0,
  "approved_candidates": 0,
  "created_at": "2026-08-17T10:30:00"
}
```

#### Obter detalhes de uma vaga
```http
GET /job/{job_id}
```

#### Listar candidatos de uma vaga
```http
GET /job/{job_id}/candidates
```

**Response (200)**
```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440001",
    "job_id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "João Silva",
    "email": "joao@example.com",
    "phone": "11999999999",
    "note": 8,
    "created_at": "2026-08-17T10:30:00"
  }
]
```

## 🏗️ Estrutura do Projeto

```
candidate-processor-api/
├── app/
│   ├── aws/                 # Integração AWS
│   │   ├── s3.py           # Upload para S3
│   │   └── sqs.py          # Fila de processamento
│   ├── config/
│   │   └── settings.py     # Configurações da aplicação
│   ├── controllers/        # Lógica de negócio
│   │   ├── job.py
│   │   └── candidates.py
│   ├── database/
│   │   ├── engine.py       # Engine do SQLAlchemy
│   │   └── url.py          # Configuração da URL do BD
│   ├── models/             # Modelos ORM
│   │   ├── job.py
│   │   ├── candidates.py
│   │   └── base.py
│   ├── routes/             # Endpoints da API
│   │   └── job.py
│   ├── schemas/            # Validação com Pydantic
│   │   ├── job.py
│   │   └── candidates.py
│   ├── dependencies/       # Dependency Injection
│   │   ├── job.py
│   │   └── candidates.py
│   └── main.py            # Aplicação FastAPI
├── alembic/               # Migrations
├── requirements.txt       # Dependências
├── run.py                # Entry point
└── .env                  # Variáveis de ambiente
```

## 💾 Modelos de Dados

### Job (Vaga)
- `id`: UUID (Primary Key)
- `filename`: String
- `status`: PENDING | PROCESSING | COMPLETED | FAILED
- `total_candidates`: Integer
- `approved_candidates`: Integer
- `created_at`: DateTime
- `completed_at`: DateTime (nullable)

### Candidates (Candidatos)
- `id`: UUID (Primary Key)
- `job_id`: UUID (Foreign Key)
- `name`: String
- `email`: String
- `phone`: String
- `note`: Integer
- `created_at`: DateTime
- **Constraint**: Unique(job_id, email)

## 🔌 Integração AWS

### S3 - Presigned URLs
Gera URLs assinadas para upload seguro de arquivos:

```python
from app.aws.s3 import generate_upload_url

url = generate_upload_url("bucket-name", "path/to/file.csv")
```

### SQS - Fila de Mensagens
Gerencia a fila de processamento de candidatos:

```python
from app.aws.sqs import send_message, receive_message, delete_message

# Enviar mensagem
send_message(queue_url, message_body)

# Receber mensagem
response = receive_message(queue_url)

# Deletar mensagem
delete_message(queue_url, receipt_handle)
```

## 🛡️ CORS

A API está configurada para aceitar requisições de:
- `http://localhost:5173` (desenvolvimento frontend)
- URL definida em `FRONT_URL` (produção)

## 📝 Migrations com Alembic

### Criar uma nova migration
```bash
alembic revision --autogenerate -m "Descrição da mudança"
```

### Aplicar migrations
```bash
alembic upgrade head
```

### Reverter migration
```bash
alembic downgrade -1
```

## 🚢 Deploy

### Docker (exemplo)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "run.py"]
```

## 🧪 Testes

Para adicionar testes ao projeto:

```bash
pip install pytest pytest-asyncio httpx
```

## 📦 Dependências Principais

- **FastAPI**: Framework web moderno
- **SQLAlchemy**: ORM para banco de dados
- **Pydantic**: Validação de dados
- **Alembic**: Migrations de banco de dados
- **boto3**: SDK AWS
- **psycopg**: Driver PostgreSQL
- **python-dotenv**: Gerenciamento de variáveis de ambiente

## 🔐 Variáveis de Ambiente

| Variável | Descrição |
|----------|-----------|
| `DATABASE_HOST` | Host do PostgreSQL |
| `DATABASE_PORT` | Porta do PostgreSQL (padrão: 5432) |
| `DATABASE_USER` | Usuário PostgreSQL |
| `DATABASE_PASSWORD` | Senha PostgreSQL |
| `DATABASE_NAME` | Nome do banco de dados |
| `AWS_PROFILE` | Perfil AWS (default: default) |
| `AWS_REGION` | Região AWS |
| `BUCKET_NAME` | Nome do bucket S3 |
| `FRONT_URL` | URL do frontend para CORS |

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👤 Autor

**Luis Gabriel Santos**
- GitHub: [@LuisG-santos](https://github.com/LuisG-santos)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📞 Suporte

Para dúvidas ou problemas, abra uma issue no repositório: [Issues](https://github.com/LuisG-santos/candidate-processor-api/issues)
