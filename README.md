# Career OS

Career OS is a modern Flask-based career management platform designed to help users organize and streamline their job search workflow.

The platform combines structured application tracking with future AI-assisted career tools such as resume-job matching, interview preparation, and career insights.

---

## ✨ Features

### Authentication
- User signup and login
- Username/email authentication
- Secure session handling with Flask-Login
- WTForms validation

### Application Tracking
- Create and manage job applications
- Track:
  - company
  - role
  - status
  - work mode
  - salary expectations
  - deadlines
  - source
  - notes

### Timeline Events
- Add application events:
  - applied
  - assessment
  - interview
  - rejected
  - offer
  - ghosted
- Automatic status syncing between timeline and application

### Dashboard
- Overview statistics
- Recent applications
- Activity timeline
- Clean SaaS-inspired UI

### Search & Filtering
- Search by:
  - company
  - role
  - location
  - source
- Filter by application status

### UI / UX
- Modern responsive interface
- Split-screen authentication pages
- Card-based dashboard layout
- Scrollable activity panels
- Priority and status pills
- Modular CSS structure

---

## 🛠 Tech Stack

### Backend
- Python
- Flask
- Flask-Login
- Flask-WTF
- SQLAlchemy
- Flask-Migrate

### Frontend
- Jinja2
- Bootstrap 5
- Custom CSS

### Database
- SQLite (development)
- PostgreSQL (planned production support)

### Future AI Stack
- OpenAI API
- LangChain
- Resume ↔ Job Description analysis
- AI interview preparation
- Career insights engine

---

## 📁 Project Structure

```text
career_os/
│
├── app/
│   ├── forms/
│   ├── models/
│   ├── routes/
│   ├── static/
│   │   ├── css/
│   │   └── images/
│   ├── templates/
│   ├── extensions.py
│   └── __init__.py
│
├── migrations/
├── instance/
├── config.py
├── server.py
└── requirements.txt
```

---

## 🚀 Current Status

Career OS is currently in active development.

Completed milestones:
- Authentication system
- Application management
- Timeline events
- Dashboard foundation
- Search & filtering
- SaaS-style UI redesign

Planned milestones:
- Resume/profile system
- AI-powered job fit analysis
- Interview preparation assistant
- Analytics & insights
- Follow-up reminders
- Production deployment

---

## 🧠 Vision

Career OS aims to become a centralized career workflow platform — combining structured job tracking with AI-assisted career guidance.

Instead of scattered spreadsheets, bookmarks, notes, and interview prep documents, Career OS provides one focused system for managing the entire job search process.

---

## ⚙️ Local Setup

### Clone repository

```bash
git clone <repo-url>
cd career_os
```

### Create virtual environment

```bash
python -m venv venv
```

### Activate virtual environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run migrations

```bash
flask db upgrade
```

### Start server

```bash
flask run
```

---

## 📌 Notes

This project is being built incrementally with a strong focus on:
- real-world workflow design
- clean architecture
- UI/UX consistency
- scalable backend structure
- practical AI integration

---

## 📷 Screenshots

> Screenshots will be added as development progresses.

---

## 📄 License

This project is currently for portfolio and educational purposes.