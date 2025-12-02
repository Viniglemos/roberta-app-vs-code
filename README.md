


# 📸 Roberta Photography Backend  
### FastAPI • MongoDB • AWS S3 • Docker • API Key Auth

This is the backend for the **Roberta Gulin Photography App**, built to manage clients, albums, and photos with secure cloud storage using AWS S3.  
Designed to support a real mobile application (React Native / Expo), this API is structured for scalability, security, and reliability.

---

## 🚀 Tech Stack

- **FastAPI** — Modern, fast, and efficient Python web framework  
- **MongoDB** — NoSQL database for clients, albums, and photos  
- **AWS S3** — Secure image storage with presigned URLs  
- **Docker & Docker Compose** — Reproducible environment and deployment  
- **Uvicorn** — ASGI server  
- **Pydantic** — Data validation and typed models  
- **API Key Authentication** — Secures critical endpoints  

---

## 📁 Project Structure

```

roberta-app-vs-code/
│
├── app.py                     # FastAPI main application
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
│
├── src/
│   ├── utils/
│   │   ├── db.py             # MongoDB connection
│   │   ├── auth.py           # API Key authentication
│   │   ├── s3.py             # S3 upload + presigned URL generation
│   │   └── ...
│   └── ...
│
└── README.md

````

---

## ⚙️ Environment Variables

Create a `.env` file (DO NOT push to GitHub):

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

# 🐳 Running with Docker (Recommended)

```bash
docker-compose up --build
```

API available at:

👉 [http://localhost:8000](http://localhost:8000)
👉 Swagger Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

---

# ▶️ Running Locally (Without Docker)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload
```

---

# 🔐 Authentication

Protected endpoints require:

```
x-api-key: your-secret-api-key
```

---

# 👥 Client Endpoints

### ➤ Create Client

```
POST /clients
```

```json
{
  "name": "Roberta",
  "email": "roberta@example.com"
}
```

### ➤ List Clients

```
GET /clients
```

---

# 📚 Album Endpoints

### ➤ Create Album

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

### ➤ List Albums

```
GET /albums
```

---

# 🖼 Photo Endpoints

### ➤ Upload Photo to an Album

```
POST /albums/{album_id}/photos
```

Multipart form fields:

* **file** → image file
* **description** → optional

Example:

```bash
curl -X POST "http://localhost:8000/albums/ALBUM_ID/photos" \
  -H "x-api-key: your-secret-api-key" \
  -F "file=@/Users/me/photo.jpg" \
  -F "description=Ceremony photo"
```

### ➤ List Photos of an Album

```
GET /albums/{album_id}/photos
```

Returns a list of photo metadata + generated presigned URLs.

---

# ☁️ AWS S3 Behavior

Uploaded files follow the structure:

```
albums/<album_id>/<timestamp>_filename
```

Each photo response includes a time-limited **presigned URL** allowing secure access.

---

# 📱 Next Steps (Mobile App Integration)

This backend will support a real mobile application built with **React Native (Expo)**:

* Upload photos directly from iPhone/Android
* Browse albums
* Client galleries
* Secure image viewing
* New events & tags

A dedicated repository for the mobile app will be released soon.

---

# 🧭 Roadmap

* [x] FastAPI backend structure
* [x] MongoDB integration
* [x] AWS S3 uploads
* [x] Presigned URLs
* [x] API Key security
* [x] CRUD for clients/albums/photos
* [ ] Backend deployment (AWS Lightsail / Elastic Beanstalk / API Gateway)
* [ ] CDN & caching
* [ ] React Native mobile app
* [ ] Admin dashboard

---

# 🤝 Contributing

Pull requests, suggestions, and improvements are welcome!
Feel free to open issues for bugs or discussions.

---

Made with ❤️ by **Vinicius G. Lemos**
Cloud Engineering Student • Python • AWS • Mobile Development

```
