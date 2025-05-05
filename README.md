# ✨ BlogToHeaven

![GitHub repo size](https://img.shields.io/github/repo-size/Kirtanmojidra/BlogToHeaven)
![License](https://img.shields.io/github/license/Kirtanmojidra/BlogToHeaven)
![Issues](https://img.shields.io/github/issues/Kirtanmojidra/BlogToHeaven)
![Stars](https://img.shields.io/github/stars/Kirtanmojidra/BlogToHeaven?style=social)

> A modern and minimalistic blogging platform to write, share, and connect — also can be used for offline and
locally hosting.

---

## 🚀 Features

- 🔐 Secure user authentication system
- 📝 Create, edit, and manage blog posts with rich text formatting
- 💬 Comment system for user engagement
- 📱 Fully responsive UI (mobile-first design)
- ⚡ Fast, lightweight, and privacy-focused (offline/local support)
- 🧠 Clean and minimal UX focused on writing
- 🗃️ Session and user management

---

## 🛠 Tech Stack

| Frontend        | Backend       | Database     | Other             |
|-----------------|---------------|--------------|--------------------|
| HTML, CSS, JS   | Python (Django) | PostgreSQL | Jinja2, QuillJs |

---

# 🚀 Installation Guide

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- [Django](https://www.djangoproject.com/) – Django
- [Tailwind](https://tailwindcss.com/) - Tailwind
- [Quilljs](https://quilljs.com/) – quillJs
- [Git](https://git-scm.com/) – Version Control System
- [Node.js](https://nodejs.org/) – JavaScript Runtime
- [npm](https://www.npmjs.com/) – Node Package Manager


## 🧪 Steps to Set Up Locally

1. **Clone the Repository**

   Open your terminal and run:

   ```bash
   git clone https://github.com/Kirtanmojidra/BlogToHeaven.git
   cd BlogToHeaven
   ```
1. **Set Up a Virtual Environment (for Python packages)**

   It's best practice to create a virtual environment for your project:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
1. **Install Python Dependencies**

   Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```
1. **Install Node.js Dependencies (for front-end themes)**
   
      Navigate to the theme/static_src directory and install the necessary Node.js packages:
   
      ```bash
      cd theme/static_src
      npm install
      ```

1. **Run Migrations (Set up the Database)**
   After setting up your virtual environment and installing dependencies, run the following commands to apply database migrations:
   ```bash
   # Generate migration files based on changes in models
   python manage.py makemigrations
   # Apply the migrations to the database
   python manage.py migrate
   ```

1. **Start Django Development Server**
   
      Start Your Development server by execute following command:
   
      ```bash
      python manage.py runserver
      ```
   
1. **Run Tailwind in Development Mode (for front-end themes)**
   
      Start the Tailwind development server:
   
      ```bash
      python manage.py tailwind start
      ```

   Make sure both servers are running before accessing the application via your browser at http://localhost:8000

## 🚀 Website Screenshot

![Homepage Screenshot](assets/blogtoheaven-homepage.png)
![Profile Screenshot](assets/blogtoheaven-Profile.png)
![Edit Blog Screenshot](assets/blogtoheaven-EditBlog.png)
![Categories Screenshot](assets/blogtoheaven-Categories.png)
![Blog Screenshot](assets/blogtoheaven-Blogs.png)