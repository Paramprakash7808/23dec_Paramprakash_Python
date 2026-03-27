# EduTracker Solutions – RESTful API
### Module 17 – Python: Django REST Framework (DRF)

A production-ready RESTful API for managing **students** and **courses** at EduTracker Solutions EdTech startup. Built with Django and Django REST Framework (DRF). Designed to connect a mobile app with a backend database.

---

## 📁 Project Structure

```
edutracker/
├── edutracker/               # Django project config
│   ├── __init__.py
│   ├── settings.py           # Settings with .env support
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI entry point (PythonAnywhere)
│
├── students/                 # Student management app
│   ├── models.py             # Student model (ManyToMany → Course)
│   ├── serializers.py        # StudentSerializer, StudentDetailSerializer
│   ├── views.py              # APIView-based CRUD + enroll/unenroll
│   ├── urls.py               # Student URL routes
│   ├── admin.py              # Django admin configuration
│   └── tests.py              # Full test suite (APIClient)
│
├── courses/                  # Course management app
│   ├── models.py             # Course model
│   ├── serializers.py        # CourseSerializer
│   ├── views.py              # APIView-based CRUD + enrolled students list
│   ├── urls.py               # Course URL routes
│   ├── admin.py              # Django admin configuration
│   └── tests.py              # Full test suite (APIClient)
│
├── manage.py
├── requirements.txt
├── .env.example              # Environment variable template
├── .gitignore
└── EduTracker_API.postman_collection.json
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/edutracker-api.git
cd edutracker-api
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
cp .env.example .env
# Edit .env and set your SECRET_KEY and other values
```

### 5. Apply Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (for Admin + Token Auth)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

API is now live at: **http://127.0.0.1:8000/**

---

## 🔐 Token Authentication

The API uses **DRF Token Authentication**.

### Get your token:
```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

**Response:**
```json
{ "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" }
```

Use this token in all subsequent requests:
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

> **Note:** `GET` requests are allowed without a token (IsAuthenticatedOrReadOnly). `POST`, `PUT`, `PATCH`, `DELETE` require a token.

---

## 📡 API Endpoints

### Student Management

| Method | Endpoint                      | Description                      | Auth Required |
|--------|-------------------------------|----------------------------------|---------------|
| GET    | `/api/students/`              | Get all students                 | No            |
| POST   | `/api/students/`              | Add a new student                | Yes           |
| GET    | `/api/students/<id>/`         | Get single student (with courses)| No            |
| PUT    | `/api/students/<id>/`         | Full update of student           | Yes           |
| PATCH  | `/api/students/<id>/`         | Partial update of student        | Yes           |
| DELETE | `/api/students/<id>/`         | Delete a student                 | Yes           |
| POST   | `/api/students/<id>/enroll/`  | Enroll student in a course       | Yes           |
| DELETE | `/api/students/<id>/enroll/`  | Unenroll student from course     | Yes           |

### Course Management

| Method | Endpoint                        | Description                       | Auth Required |
|--------|---------------------------------|-----------------------------------|---------------|
| GET    | `/api/courses/`                 | Get all courses                   | No            |
| POST   | `/api/courses/`                 | Add a new course                  | Yes           |
| GET    | `/api/courses/<id>/`            | Get single course                 | No            |
| PUT    | `/api/courses/<id>/`            | Full update of course             | Yes           |
| PATCH  | `/api/courses/<id>/`            | Partial update of course          | Yes           |
| DELETE | `/api/courses/<id>/`            | Delete a course                   | Yes           |
| GET    | `/api/courses/<id>/students/`   | List students enrolled in course  | No            |

### Auth

| Method | Endpoint              | Description          |
|--------|-----------------------|----------------------|
| POST   | `/api/auth/token/`    | Get auth token       |

---

## 🧪 Testing with curl

### Get all students
```bash
curl http://127.0.0.1:8000/api/students/
```

### Create a new student
```bash
curl -X POST http://127.0.0.1:8000/api/students/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "Ravi",
    "last_name": "Patel",
    "email": "ravi.patel@example.com",
    "phone": "9876543210",
    "enrolled_courses": []
  }'
```

### Get a single student
```bash
curl http://127.0.0.1:8000/api/students/1/
```

### Update student details (PATCH)
```bash
curl -X PATCH http://127.0.0.1:8000/api/students/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"phone": "1234567890"}'
```

### Delete a student
```bash
curl -X DELETE http://127.0.0.1:8000/api/students/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Create a course
```bash
curl -X POST http://127.0.0.1:8000/api/courses/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Django REST Framework",
    "description": "Build REST APIs with DRF.",
    "instructor": "Alice Smith",
    "duration_weeks": 6,
    "is_active": true
  }'
```

### Enroll student in a course
```bash
curl -X POST http://127.0.0.1:8000/api/students/1/enroll/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1}'
```

### Unenroll student from a course
```bash
curl -X DELETE http://127.0.0.1:8000/api/students/1/enroll/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"course_id": 1}'
```

### List students enrolled in a course
```bash
curl http://127.0.0.1:8000/api/courses/1/students/
```

---

## 📬 Postman

Import `EduTracker_API.postman_collection.json` into Postman.

1. Open Postman → **Import** → select the file
2. Set the `base_url` variable to `http://127.0.0.1:8000`
3. Run **"Get Auth Token"** first, copy the token value
4. Set the `token` collection variable
5. All other requests are ready to run

---

## 🖥️ Django Admin

Visit: **http://127.0.0.1:8000/admin/**

Log in with your superuser credentials. Admin supports:
- **Students**: view/add/edit/delete with ManyToMany course picker
- **Courses**: view/add/edit/delete with student enrollment count

---

## 🚀 Deployment – PythonAnywhere

### Steps:

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit – EduTracker API"
git remote add origin https://github.com/yourusername/edutracker-api.git
git push -u origin main
```

2. **On PythonAnywhere** (via Bash console):
```bash
git clone https://github.com/yourusername/edutracker-api.git
cd edutracker-api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env: set SECRET_KEY, DEBUG=False, ALLOWED_HOSTS=yourusername.pythonanywhere.com
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

3. **Web App config on PythonAnywhere:**
   - Source code: `/home/yourusername/edutracker-api`
   - Working directory: `/home/yourusername/edutracker-api`
   - WSGI file path: edit the PythonAnywhere-generated WSGI file:
     ```python
     import os
     import sys
     path = '/home/yourusername/edutracker-api'
     if path not in sys.path:
         sys.path.append(path)
     os.environ['DJANGO_SETTINGS_MODULE'] = 'edutracker.settings'
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
   - Virtual env: `/home/yourusername/edutracker-api/venv`

4. Click **Reload** – your API is live at `https://yourusername.pythonanywhere.com/`

---

## 🧠 Reflective Thinking

### 1. How would you add real-time notifications (e.g., when a student enrolls)?

Use **Django Channels** with **WebSockets** for real-time push notifications.

**Implementation approach:**
- Install `channels` and `channels-redis`, configure `ASGI_APPLICATION` and `CHANNEL_LAYERS` with a Redis backend.
- Create a `NotificationConsumer` (WebSocket consumer) in a new `notifications` app.
- When a student enrolls (inside `StudentEnrollView.post()`), send a message to the relevant channel group:
  ```python
  from channels.layers import get_channel_layer
  from asgiref.sync import async_to_sync

  channel_layer = get_channel_layer()
  async_to_sync(channel_layer.group_send)(
      f"course_{course_id}_notifications",
      {"type": "enrollment.notification", "student": str(student), "course": str(course)}
  )
  ```
- The mobile app connects to `ws://yourdomain.com/ws/notifications/` and receives live enrollment events.
- Alternatively, for simpler one-way push (no WebSocket on client), use **Django Signals** + a **push notification service** (e.g., Firebase Cloud Messaging) to send a push to the instructor's device when a student enrolls.

---

### 2. How would you allow video course uploads with file size limits?

Use **Django's FileField/FileSystemStorage** with size validation, or offload to **cloud storage**.

**Implementation approach:**
- Add a `video` FileField to the `Course` model:
  ```python
  video = models.FileField(upload_to='course_videos/', blank=True, null=True)
  ```
- Add a custom validator for file size (e.g., 500 MB limit):
  ```python
  from django.core.exceptions import ValidationError

  def validate_video_size(file):
      max_size_mb = 500
      if file.size > max_size_mb * 1024 * 1024:
          raise ValidationError(f"Video file must be under {max_size_mb} MB.")
  ```
- Apply validator: `video = models.FileField(validators=[validate_video_size], ...)`
- For production, use **django-storages** with **AWS S3** or **Cloudinary** to store large files outside the server:
  ```bash
  pip install django-storages boto3
  ```
- Use **chunked uploads** (via `django-chunked-upload` or a multipart S3 presigned URL) for large files to avoid request timeouts.
- Add `MultiPartParser` to DRF settings so the API can accept `multipart/form-data` from the mobile app.

---

### 3. How would you handle rate-limiting for high traffic from frontend/mobile?

Use **django-ratelimit** or DRF's **throttling classes** to protect the API.

**Implementation approach:**

**Option A – DRF Built-in Throttling (quick setup):**
```python
# In settings.py
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',   # unauthenticated users
        'rest_framework.throttling.UserRateThrottle',   # authenticated users
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
    }
}
```

**Option B – Per-view throttling for sensitive endpoints:**
```python
from rest_framework.throttling import UserRateThrottle

class EnrollmentRateThrottle(UserRateThrottle):
    rate = '10/minute'  # max 10 enrollments per minute per user

class StudentEnrollView(APIView):
    throttle_classes = [EnrollmentRateThrottle]
```

**Option C – Infrastructure-level (production best practice):**
- Use **Nginx** rate limiting (`limit_req_zone`) in front of the Django app.
- Use a **CDN with WAF** (e.g., Cloudflare) to block abusive traffic before it hits Django.
- Use **Redis** as the throttle backend for shared state across multiple server instances (horizontal scaling).

The best production setup combines DRF throttling (app-level, user-aware) + Nginx/Cloudflare (infrastructure-level, IP-based) for full coverage.

---

## 🛠️ Key Technologies

- **Django 4.2** – web framework
- **Django REST Framework 3.15** – API toolkit (Serializers, APIView, Token Auth)
- **python-dotenv** – `.env` file support
- **SQLite** (dev) / **PostgreSQL** (production)
- **Token Authentication** – DRF built-in
- **Django Admin** – full model management UI
- **Postman / curl** – API testing

---

## 📝 License

Built for EduTracker Solutions – Module 17 Assessment.
