# WriteSphere – Django Blogging Platform

A full-stack blogging platform built with Django + MySQL, developed for WriteHub Community.

---

## Features

- **User Management**: Register, login, logout, session handling, role-based access (Admin / Author / Reader)
- **Blog Management**: Create, edit, delete posts with rich-text editor (CKEditor), cover images, categories, tags
- **Blog Listing**: Filter by author, category, date range, search
- **Interactions**: Like/unlike posts, add/edit/delete comments, follow/unfollow authors
- **Responsive Design**: Bootstrap 5 with custom CSS
- **Admin Panel**: Fully customized Django admin
- **Deployment Ready**: PythonAnywhere + MySQL config, `.env` secrets management, GitHub-ready

---

## Tech Stack

- **Backend**: Django 4.2, Python 3.10+
- **Database**: MySQL (via mysqlclient)
- **Frontend**: HTML5, CSS3, Bootstrap 5, Vanilla JS
- **Rich Text**: CKEditor 4 (django-ckeditor)
- **Tags**: django-taggit
- **Static Files**: WhiteNoise

---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/writesphere.git
cd writesphere
```

### 2. Create and activate virtual environment

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure `.env`

Copy the `.env` file and update your settings:

```env
DEBUG=True
SECRET_KEY=your-very-secret-key-change-in-production
DB_NAME=writesphere_db
DB_USER=root
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=3306
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Create MySQL Database

```sql
CREATE DATABASE writesphere_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Collect static files

```bash
python manage.py collectstatic
```

### 9. Run the server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## PythonAnywhere Deployment

### 1. Upload your code

Push to GitHub and pull on PythonAnywhere, or upload the zip file.

### 2. Set up virtual environment on PythonAnywhere

```bash
cd ~
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure MySQL on PythonAnywhere

Go to **Databases** tab → Create a MySQL database (e.g. `yourusername$writesphere_db`)

Update `.env`:
```env
DB_NAME=yourusername$writesphere_db
DB_USER=yourusername
DB_PASSWORD=yourmysqlpassword
DB_HOST=yourusername.mysql.pythonanywhere-services.com
DB_PORT=3306
ALLOWED_HOSTS=yourusername.pythonanywhere.com
DEBUG=False
```

### 4. Configure WSGI on PythonAnywhere

In the **Web** tab, set the WSGI configuration file to:

```python
import os
import sys

path = '/home/yourusername/writesphere'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'writesphere.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### 5. Static & Media files

In the **Web** tab:
- Static files URL: `/static/` → Directory: `/home/yourusername/writesphere/staticfiles/`
- Media files URL: `/media/` → Directory: `/home/yourusername/writesphere/media/`

### 6. Run migrations and collectstatic

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

### 7. Reload the web app

Click **Reload** in the Web tab.

---

## Project Structure

```
writesphere/
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
├── writesphere/           # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/              # User management app
│   ├── models.py          # CustomUser, Follow
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── admin.py
├── blog/                  # Blog app
│   ├── models.py          # Post, Category, Comment, Like
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   └── context_processors.py
├── templates/
│   ├── base.html
│   ├── accounts/
│   │   ├── register.html
│   │   ├── login.html
│   │   ├── profile.html
│   │   └── edit_profile.html
│   └── blog/
│       ├── home.html
│       ├── post_list.html
│       ├── post_detail.html
│       ├── post_form.html
│       ├── post_confirm_delete.html
│       ├── comment_edit.html
│       ├── dashboard.html
│       ├── category_posts.html
│       └── tag_posts.html
├── static/
│   ├── css/style.css
│   └── js/main.js
└── media/                 # User uploads (auto-created)
```

---

## Database Schema

| Model | Key Fields |
|---|---|
| CustomUser | username, email, role (admin/author/reader), bio, profile_picture |
| Follow | follower → CustomUser, following → CustomUser |
| Category | name, slug, description |
| Post | title, slug, author, content (RichText), cover_image, category, tags, status |
| Comment | post, author, content, parent (for replies), is_approved |
| Like | post, user |

---

## Admin Access

Visit `/admin/` and log in with your superuser credentials.

The admin panel includes:
- User management with role assignment
- Post management with bulk publish/draft
- Comment moderation (approve/disapprove)
- Category management
- Like and Follow records

---

## GitHub Setup

```bash
git init
git add .
git commit -m "Initial commit: WriteSphere Django project"
git remote add origin https://github.com/yourusername/writesphere.git
git push -u origin main
```

> Note: `.env` is in `.gitignore` — never commit secrets to GitHub.
