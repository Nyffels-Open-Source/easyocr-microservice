# 🧠 ocr-microservice

**OCR Service for Document Digitization Pipelines**  
Open source microservice developed by [Nyffels BV](https://nyffels.be)  
Contact: chesney@nyffels.be

GitHub Repository: [https://github.com/Nyffels-Open-Source/ocr-microservice](https://github.com/Nyffels-Open-Source/ocr-microservice)  
DockerHub: [https://hub.docker.com/repository/docker/nyffels/ocr-microservice](https://hub.docker.com/repository/docker/nyffels/ocr-microservice)  
Docker Image: `nyffels/ocr-microservice:latest`

---

## 🔍 Overview

`ocr-microservice` is a production-grade OCR API using FastAPI + EasyOCR.  
It extracts text from individual image files or a ZIP archive, with automatic language detection.

---

## 📦 Features

- Extracts text from:
  - One or more image files (PNG, JPEG, etc.)
  - ZIP file containing images
- Auto language detection (supports: `en`, `nl`, `fr`, `de`, `es`, `it`, `pt`)
- Average OCR confidence reporting
- REST API via FastAPI with Swagger UI
- Fully containerized with preloaded OCR models

---

## ⚠️ Security Notice

> This service has **no built-in authentication or authorization**.  
> It is meant to run inside a private network or behind a secured reverse proxy.

---

## 🚀 Quickstart (Docker)

```bash
docker pull nyffels/ocr-microservice:latest

docker run -d \
  -p 8000:8000 \
  --name ocr-service \
  nyffels/ocr-microservice:latest
```

Access Swagger UI at: `http://localhost:8000/docs`

---

## 🔧 API Usage

### `POST /ocr`
OCR for one or more uploaded image files.

#### Request
- **Type:** `multipart/form-data`
- **Field:** `files` (multiple images)

#### Example
```bash
curl -X POST http://localhost:8000/ocr \
  -F "files=@page1.jpg" \
  -F "files=@page2.png"
```

---

### `POST /ocr-zip`
OCR for a ZIP archive containing images.

#### Request
- **Type:** `multipart/form-data`
- **Field:** `file` (ZIP archive)

#### Example
```bash
curl -X POST http://localhost:8000/ocr-zip \
  -F "file=@document-pages.zip"
```

---

### `GET /health`
Returns `{"status": "ok"}`

---

## 🛠 Tech Stack

- Python 3.11
- FastAPI
- EasyOCR
- langdetect
- Docker

---

## 📂 Folder Structure

```
ocr-microservice/
├── app/
│   ├── main.py           # FastAPI app
│   ├── ocr_service.py    # OCR logic with EasyOCR
│   └── schema.py         # Pydantic models
├── tests/
│   └── data/test-image.png
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome!  
Please open an issue first before submitting a pull request.

Let's make document processing smarter 📄✨

---

## 📄 License

MIT License © 2025 Nyffels BV

See [`LICENSE`](./LICENSE) for full terms.