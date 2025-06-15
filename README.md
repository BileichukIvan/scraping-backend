# 🕸️ Scrapy + 🚀 FastAPI + 🐘 PostgreSQL Backend

This project uses **Scrapy** to scrape product data and **FastAPI** to provide a REST API for accessing the collected information.

---

## 🚀 Getting Started
### 1. Clone the repository

```bash
    git clone https://https://github.com/BileichukIvan/scraping-backend
    cd scraping_backend
```

### 2. Create and activate a virtual environment

```bash
    python -m venv .venv
    source .venv/bin/activate    # Linux/macOS
    .venv\Scripts\activate 
```

### 3. Install dependencies
```bash
    pip install -r requirements.txt
```

### 🕷️ Scrapy: Collect Product Data
```bash
    cd menu_scraper
    scrapy crawl menu_spider -o products.json
```

### 🌐 FastAPI: Run API Server
```bash
    cd backend
    uvicorn main:app --reload 
```

### Open in your browser:

* Swagger UI: http://localhost:8000/docs
