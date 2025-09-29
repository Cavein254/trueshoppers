# Project Nexus

A scalable and extensible **Django-based e-commerce backend** that powers shops, products, categories, and user management.
This project integrates modern tooling for **authentication, API documentation, caching, and asynchronous tasks**.

---

## 🚀 Features

- **Django** – High-level, scalable Python web framework.
- **PostgreSQL** – Optimized relational database for performance and reliability.
- **JWT Authentication** – Secure login & token-based user sessions.
- **Swagger/OpenAPI** – Interactive API documentation & testing.
- **Redis** – In-memory store for caching and session management.
- **RabbitMQ** – Message broker for background jobs & async tasks.
- **Custom User Model** – Email-based authentication with public IDs.
- **Shop & Product Models** – Supports categories, product images, and unique SKUs.
- **Image Processing** – Auto WebP conversion & thumbnail generation with `django-imagekit`.

## 🏗️ Models Overview

### **Shop**

- Owned by a user
- Supports logos, covers, descriptions
- Auto-slug generation

### **Category**

- Hierarchical (parent/child support)
- Auto-slug generation

### **Product**

- Linked to a shop & categories
- Auto SKU + unique slug per shop
- Supports stock & pricing
- Constraints ensure unique SKU and slug per shop

### **ProductImage**

- Linked to a product
- Auto WebP conversion on upload
- Dynamic 200x200 thumbnails

### **CustomUser**

- Email as username
- Public ID with `usr_` prefix
- Supports staff/superuser flags

## ![models](./img/trueshoppers.png)

## ⚙️ Tech Stack

- **Backend:** Django, Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** JWT (access + refresh tokens)
- **Caching & Queues:** Redis + RabbitMQ
- **Documentation:** Swagger / OpenAPI

---

## 📖 API Documentation

Swagger UI is available after running the project:

`http://localhost:8000/api/v1/docs/swagger/`

---

## 🛠️ Installation & Setup

### 1. Clone Repository

```bash
git clone git@github.com:Cavein254/trueshoppers.git
cd trueshoppers
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Environment Variables

```bash
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/ecommerce
REDIS_URL=redis://localhost:6379/0
RABBITMQ_URL=amqp://guest:guest@localhost:5672/
```

### 5. Apply Migrations

```bash
python manage.py migrate
```

### 7. Run Server

```bash
python manage.py runserver
```
