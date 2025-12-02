


# 📸 Roberta Photography Backend  
### FastAPI • MongoDB • AWS S3 • Docker • API Key Auth

Backend desenvolvido para o aplicativo de fotografia **Roberta Gulin Photo App**, permitindo gerenciar clientes, álbuns e fotos — com upload seguro para a AWS S3 e arquitetura escalável para uso real no dia a dia.

---

## Composiçao 

- **FastAPI** — API moderna, rápida e eficiente  
- **MongoDB** — Banco NoSQL para clientes, álbuns e fotos  
- **AWS S3** — Armazenamento seguro de imagens via presigned URLs  
- **Docker & Docker Compose** — Facilita execução e deploy  
- **Uvicorn** — Servidor ASGI  
- **Pydantic** — Tipagem e validação  
- **API Key Authentication** — Segurança para endpoints sensíveis  

---

## 📁 Estrutura do Projeto

```

roberta-app-vs-code/
│
├── app.py                     # Aplicação FastAPI
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── utils/
│   │   ├── db.py             # Conexão com MongoDB
│   │   ├── auth.py           # Autenticação por API Key
│   │   ├── s3.py             # Upload e URL presignada (AWS)
│   │   └── ...
│   └── ...
│
└── README.md

````

---

## Configuração — Arquivo `.env`

Crie um arquivo `.env` (não enviar ao GitHub):

```env
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=roberta_app

API_KEY=your-secret-api-key

AWS_ACCESS_KEY_ID=xxxxxxx
AWS_SECRET_ACCESS_KEY=xxxxxxx
AWS_REGION=us-east-1
S3_BUCKET_NAME=roberta-app
````

---

# 🐳 Executando com Docker (Recomendado)

```bash
docker-compose up --build
```

API disponível em:

👉 [http://localhost:8000](http://localhost:8000)
👉 Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)

---

# Executando Localmente (sem Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

---

# 🔐 Autenticação Necessária

Envie o header:

```
x-api-key: your-secret-api-key
```

Para endpoints protegidos (como upload de fotos).

---

# 👥 Endpoints — Clientes

### ➤ Criar Cliente

```
POST /clients
```

Body:

```json
{
  "name": "Roberta",
  "email": "roberta@example.com"
}
```

### ➤ Listar Clientes

```
GET /clients
```

---

# Endpoints — Álbuns

### ➤ Criar Álbum

```
POST /albums
```

```json
{
  "title": "Wedding – Sydney",
  "client_name": "Roberta",
  "event_date": "2025-11-13",
  "tags": ["wedding", "australia"]
}
```

### ➤ Listar Álbuns

```
GET /albums
```

---

# Endpoints — Fotos

### ➤ Upload de Foto para Álbum

```
POST /albums/{album_id}/photos
```

Multipart form:

* `file` → arquivo da foto
* `description` → opcional

Exemplo:

```bash
curl -X POST "http://localhost:8000/albums/ALBUM_ID/photos" \
  -H "x-api-key: your-secret-api-key" \
  -F "file=@/Users/me/photo.jpg" \
  -F "description=Foto da cerimônia"
```

### ➤ Listar Fotos de um Álbum

```
GET /albums/{album_id}/photos
```

Retorna lista com URLs presignadas.

---

# Como funciona o S3

As fotos são armazenadas em:

```
albums/<album_id>/<timestamp>_filename
```

A API retorna uma URL temporária (presigned) para acesso seguro à imagem.

---

# 📱 Próximos Passos

* Integração com app mobile (React Native / Expo)
* Deploy em AWS (Lightsail, Elastic Beanstalk ou API Gateway + Lambda)
* CDN & Cache
* Dashboard administrativo web

---

# 🧭 Roadmap

* [x] Backend FastAPI
* [x] MongoDB + Models
* [x] Upload AWS S3
* [x] Presigned URLs
* [x] API Key Auth
* [x] CRUDs principais
* [ ] Deploy AWS
* [ ] Mobile App
* [ ] Painel Web

---

# Contribuições

Contribuições e sugestões são bem-vindas!
Abra um PR ou Issue.

---

Feito com ❤️ por **Vinicius G. Lemos**
Cloud Engineering Student • AWS • Python • Mobile Dev

```
