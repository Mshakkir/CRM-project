# 🧩 CRM Project

A full-featured Customer Relationship Management (CRM) web application built using Django and MySQL. It supports user registration, email notifications, media uploads, and more—ideal for small to medium business use cases.

---

## 🚀 Features

- ✅ User registration with custom user model
- ✅ Admin dashboard (Django Admin)
- ✅ Email sending via Gmail SMTP
- ✅ Static & media file handling
- ✅ Modular structure with `CRM_APP`
- ✅ Responsive UI using templates (HTML/CSS)
- ✅ MySQL database integration

---

## 🛠️ Tech Stack

- **Framework**: Django 3.2
- **Language**: Python 3.x
- **Database**: MySQL
- **Frontend**: HTML, CSS
- **Email**: Gmail SMTP
- **ORM**: Django ORM
- **Custom User Model**: Implemented in `CRM_APP.User`
- **Dependency Management**: `pip`

---

## 📁 Folder Structure
CRM_project/ ├── CRM_APP/ # Custom Django app ├── CRM_project/ # Project config folder │ ├── init.py # MySQL setup using PyMySQL │ ├── asgi.py # ASGI configuration │ ├── settings.py # Project settings │ ├── urls.py # URL routing │ └── wsgi.py # WSGI configuration ├── Templates/ # HTML template files ├── static/ # CSS, JS, Images ├── media/ # Uploaded media files ├── manage.py
