# 📘 Homework Submission API - Documentation

## 📌 Overview

This API allows **students** to submit homework and **teachers** to grade submissions.  
It includes authentication, role-based access control, and filters for viewing submissions.

---

## 🚀 Setup Instructions

### **1️⃣ Install Dependencies**

Ensure you have Python and Django installed.  
Run the following command to install dependencies:

```sh
pip install -r requirements.txt
```

Run the following commands to set up the database:

```sh
python manage.py makemigrations api
python manage.py migrate
```

### **2️⃣ Set Up**

A superuser is needed to create students and teachers through the Django Admin Panel.

```sh
python manage.py createsuperuser
```

Enter a username, email, and password when prompted.

Run the Django development server:

```sh
python manage.py runserver
```

The API will be available at: http://127.0.0.1:8000/

Log in using the superuser credentials.
We can use the Admin UI to create Teachers and Students.
In order to do this, create two Users (with Username, Password, Name)

Then, Create a Teacher and Student and link it to the User.
Now, the users can authenticate via API using their token (can be created via ui)

## 📌 API Endpoints

For ease of use to test each of the endpoints, I have created and included a postman collection that I was using during development:

```
https://api.postman.com/collections/31854357-11da8de4-6f6b-45a5-a77d-c26c0983a9f2?access_key=PMAT-01JP4WHMFCEXACWRQDKH7MFMF6
```

## **1️⃣ Students**

### Headers

`Authorization: Token {{student_token}}`

`Content-Type: application/json`

### Submit Homework

Method: `POST`

URL: `/api/submissions/create/`

Body (JSON):

```json
{
  "assignment": 1,
  "homework_text": "Here is my math homework."
}
```

Response (JSON):

```json
{
  "id": 1,
  "assignment": 1,
  "student": 2,
  "submission_date": "2025-03-12T12:00:00Z",
  "homework_text": "Here is my math homework.",
  "final_grade": "ungraded",
  "teacher_notes": null
}
```

### View Own Submissions

Method: `GET`

URL: `/api/submissions/`

Filters:

?final_grade=A → Filter by grade

?search=Math → Filter by assignment name

## **2️⃣ Teachers**

Headers

`Authorization: Token {{teacher_token}}`

`Content-Type: application/json`

### View All Assignments

Method: `GET`

URL: `/api/assignments/`

### Create a New Assignment

Method: `POST`

URL: `/api/assignments/`

Body (JSON):

```json
{
  "title": "Science Project",
  "description": "Write a 5-page science report."
}
```

Response (JSON):

```json
{
  "id": 2,
  "title": "Science Project",
  "description": "Write a 5-page science report.",
  "created_at": "2025-03-12T13:00:00Z",
  "created_by": 3
}
```

### View All Student Submissions

Method: `GET`

URL: `/api/submissions/`

Filters:

?student_name=john

?start_date=2024-03-01&end_date=2024-03-10

### Grade a Submission

Method: `PATCH`

URL: `/api/submissions/{{submission_id}}/update/`

Body (JSON):

```json
{
  "final_grade": "A",
  "teacher_notes": "Excellent work!"
}
```

Response (JSON):

```json
{
  "id": 1,
  "assignment": 1,
  "student": 2,
  "submission_date": "2025-03-12T12:00:00Z",
  "homework_text": "Math homework answers.",
  "final_grade": "A",
  "teacher_notes": "Excellent work!",
  "grading_date": "2025-03-13T14:00:00Z"
}
```

## 🚀 Running Tests

```sh
python manage.py test api
```
