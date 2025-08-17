# Capstone_Project_ALX
# QTrack – Automated QA Ticketing System


## 📌 Overview
QTrack is an **automated QA issue tracking system** built with **Django** and **Django REST Framework**.  
It helps teams report, track, and manage issues efficiently.  

The app provides both:
- A **web dashboard** for quick issue management.
- A **REST API** for integration with other systems.

QTrack is designed as part of a capstone project but can be extended into a real-world QA tool.

---

## ✨ Features
- 📝 Submit and manage issues (title, description, status, priority)
- 📊 Dashboard with issue statistics
- 🔍 Filter issues by status/priority
- 📂 Export issues as CSV
- 🔑 Authentication for API usage
- 🌐 REST API for third-party integration
- (Optional/Future) 📧 Email notifications for new issues
- (Optional/Future) 💬 Comment system for collaborative QA
- (Optional/Future) 📈 Charts for issue trends

---

## 🛠 Tech Stack
- **Backend:** Django, Django REST Framework
- **Frontend:** Django templates + Bootstrap
- **Database:** SQLite (development), PostgreSQL (production ready)
- **Deployment:** Heroku / Render / Railway (TBD)
- **Other Tools:** Git, Docker (optional later), Postman (API testing)

---

## 📐 Database Schema (ERD)
****
---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- pip
- virtualenv (recommended)

### Installation
```bash
# Clone the repository
git clone https://github.com/<your-username>/qtrack.git
cd qtrack

# Create virtual environment
python -m venv venv
source venv/bin/activate  # on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Run server
python manage.py runserver
