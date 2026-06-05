# 🐦 Django Tweet App — CI/CD DevOps Project

![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-2088FF?logo=github-actions&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx&logoColor=white)
![Django](https://img.shields.io/badge/Django-Web%20Framework-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)

A full-featured Twitter/tweet clone built with **Django**, deployed on a live server with a production-grade **CI/CD pipeline** using **GitHub Actions**, **Docker**, **Nginx**, and **Gunicorn**.

🌐 **Live Demo:** [https://zaid-devops.duckdns.org](https://zaid-devops.duckdns.org)
📦 **Repository:** [github.com/MuhammadZaid11/Django_DevOps_CI-CD_project](https://github.com/MuhammadZaid11/Django_DevOps_CI-CD_project)

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [CI/CD Pipeline](#cicd-pipeline)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Local Development](#local-development)
  - [Docker Setup](#docker-setup)
- [Environment Variables](#environment-variables)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## ✨ Features

- 📝 Create, view, and delete tweets
- 👤 User authentication (register / login / logout)
- 🔐 Secure session management
- 📱 Responsive UI
- 🚀 Automated deployments via GitHub Actions
- 🐳 Fully containerized with Docker
- 🔁 Zero-downtime deploys via Gunicorn + Nginx

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Django (Python) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Web Server** | Nginx (reverse proxy) |
| **App Server** | Gunicorn (WSGI) |
| **Containerization** | Docker & Docker Compose |
| **CI/CD** | GitHub Actions |
| **Hosting** | VPS / Cloud Server |
| **DNS** | DuckDNS |

---

## 🏗 Architecture

```
                        ┌─────────────────────────────────────────┐
                        │              VPS / Server               │
  Internet              │                                         │
    │                   │   ┌─────────┐       ┌──────────────┐   │
    │   HTTP/HTTPS       │   │         │       │              │   │
    └───────────────────►│   │  Nginx  ├──────►│   Gunicorn   │   │
                        │   │ :80/443 │       │   :8000      │   │
                        │   └─────────┘       └──────┬───────┘   │
                        │                            │           │
                        │                     ┌──────▼───────┐   │
                        │                     │ Django App   │   │
                        │                     │ (Container)  │   │
                        │                     └──────┬───────┘   │
                        │                            │           │
                        │                     ┌──────▼───────┐   │
                        │                     │   Database   │   │
                        │                     └──────────────┘   │
                        └─────────────────────────────────────────┘
```

**Request Flow:**
1. User hits the domain → Nginx receives the request
2. Nginx forwards traffic to Gunicorn on port 8000
3. Gunicorn runs the Django WSGI app
4. Django processes the request, queries the DB, and returns a response

---

## 🔄 CI/CD Pipeline

Every push to the `main` branch triggers the following automated workflow:

```
Push to main
     │
     ▼
┌─────────────┐
│   GitHub    │
│   Actions   │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────────┐
│  Run Tests  ├────►│ Build Docker├────►│  SSH Deploy to  │
│  (pytest)   │     │   Image     │     │    Server       │
└─────────────┘     └─────────────┘     └────────┬────────┘
                                                 │
                                    ┌────────────▼────────────┐
                                    │  docker compose pull    │
                                    │  docker compose up -d   │
                                    │  (zero-downtime swap)   │
                                    └─────────────────────────┘
```

### Workflow Steps (`.github/workflows/deploy.yml`):

1. **Checkout** — pulls latest code
2. **Test** — runs Django test suite
3. **Build** — builds Docker image
4. **Push** — pushes image to Docker Hub / registry
5. **Deploy** — SSHs into the server and runs `docker compose up -d`

---

## 📁 Project Structure

```
Django_DevOps_CI-CD_project/
│
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions CI/CD workflow
│
├── tweet/                      # Main Django app
│   ├── migrations/
│   ├── templates/
│   │   └── tweet/
│   ├── models.py               # Tweet model
│   ├── views.py                # CRUD views
│   ├── urls.py
│   └── forms.py
│
├── accounts/                   # Auth app (login/register)
│   ├── templates/
│   ├── views.py
│   └── urls.py
│
├── myproject/                  # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── nginx/
│   └── default.conf            # Nginx reverse proxy config
│
├── Dockerfile                  # App container definition
├── docker-compose.yml          # Multi-container orchestration
├── requirements.txt
├── manage.py
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

Make sure you have the following installed:

- [Python 3.x](https://www.python.org/)
- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/)
- [Git](https://git-scm.com/)

---

### Local Development

```bash
# 1. Clone the repository
git clone https://github.com/MuhammadZaid11/Django_DevOps_CI-CD_project.git
cd Django_DevOps_CI-CD_project

# 2. Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (optional)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000` in your browser.

---

### Docker Setup

```bash
# Build and start all services
docker compose up --build

# Run in detached mode
docker compose up -d

# Stop all containers
docker compose down

# View logs
docker compose logs -f
```

---

## 🔐 Environment Variables

Create a `.env` file in the project root:

```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,localhost

# Database (if using PostgreSQL)
DB_NAME=tweet_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=db
DB_PORT=5432
```

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.

---

## ☁️ Deployment

### Server Setup (one-time)

```bash
# Install Docker on the server
sudo apt update && sudo apt install docker.io docker-compose -y

# Clone the repo on the server
git clone https://github.com/MuhammadZaid11/Django_DevOps_CI-CD_project.git

# Set up your .env file
cp .env.example .env
nano .env  # fill in values

# Start the stack
docker compose up -d
```

### GitHub Actions Secrets

Add the following secrets in your GitHub repo (`Settings → Secrets and variables → Actions`):

| Secret | Description |
|---|---|
| `DOCKER_USERNAME` | Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password or access token |
| `SSH_HOST` | Your server's IP or domain |
| `SSH_USER` | SSH username (e.g. `ubuntu`) |
| `SSH_PRIVATE_KEY` | Private SSH key for the server |

Once configured, every push to `main` auto-deploys to your server. 🎉

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

1. Fork the project
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 👨‍💻 Author

**Muhammad Zaid**
- GitHub: [@MuhammadZaid11](https://github.com/MuhammadZaid11)
- Live Project: [zaid-devops.duckdns.org](https://zaid-devops.duckdns.org)

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ as a DevOps learning project — Django + Docker + GitHub Actions + Nginx + Gunicorn
