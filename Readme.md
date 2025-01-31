# FAQ Management System

This is a Django-based FAQ management system with support for multi-language translations, caching, and a REST API.

## Features
- Create, update, delete, and retrieve FAQs.
- Multi-language support (English, Hindi, Bengali, Spanish, Telugu, Sanskrit).
- Caching using Redis for improved performance.
- REST API for managing FAQs.

---

## Prerequisites
- Docker and Docker Compose installed on your machine.

---

## Setup

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/faq-management-system.git
cd faq-management-system
```

2. Build and Run the Docker Containers
```bash
docker-compose up --build
```
The application will be available at http://localhost:8000.

3. Apply Migrations
Run the following command to apply database migrations:

```bash
docker-compose exec web python manage.py migrate
```

4. Create a Superuser
Create a superuser to access the Django admin panel:

```bash
docker-compose exec web python manage.py createsuperuser
```
5. Access the Admin Panel
Visit http://localhost:8000/admin and log in with your superuser credentials.

API Usage
Base URL
All API endpoints are available under http://localhost:8000/api/.

1. Fetch FAQs
Fetch all FAQs in the specified language.

Endpoint:
GET /api/faqs/
Query Parameters
lang (optional): Language code (en, hi, bn, es, te, sa). Defaults to English (en).

Example Requests
Fetch FAQs in English:

```bash
curl http://localhost:8000/api/faqs/
```
Fetch FAQs in Hindi:

```bash
curl http://localhost:8000/api/faqs/?lang=hi
```

Fetch FAQs in Spanish:

```bash
curl http://localhost:8000/api/faqs/?lang=es
```
Example Response
json:
```json
[
    {
        "id": 1,
        "question": "What is Django?",
        "answer": "<p>Django is a web framework.</p>"
    }
]
```
2. Create an FAQ
Create a new FAQ.

Endpoint
POST /api/faqs/
Request Body
```json
{
    "question": "What is Python?",
    "answer": "<p>Python is a programming language.</p>"
}
```
Example Request
```bash
curl -X POST http://localhost:8000/api/faqs/ \
-H "Content-Type: application/json" \
-d '{
    "question": "What is Python?",
    "answer": "<p>Python is a programming language.</p>"
}'
```
Example Response
```json
{
    "id": 2,
    "question": "What is Python?",
    "answer": "<p>Python is a programming language.</p>"
}
```

3. Retrieve an FAQ
Retrieve a specific FAQ by its ID.

Endpoint
GET /api/faqs/{id}/
Example Request
```bash
curl http://localhost:8000/api/faqs/1/
```
Example Response
```json
{
    "id": 1,
    "question": "What is Django?",
    "answer": "<p>Django is a web framework.</p>"
}
```
4. Update an FAQ
Update an existing FAQ by its ID.

Endpoint
PUT /api/faqs/{id}/
Request Body
```json
{
    "question": "What is Django?",
    "answer": "<p>Django is a high-level Python web framework.</p>"
}
```
Example Request
```bash
curl -X PUT http://localhost:8000/api/faqs/1/ \
-H "Content-Type: application/json" \
-d '{
    "question": "What is Django?",
    "answer": "<p>Django is a high-level Python web framework.</p>"
}'
```
Example Response
```json
{
    "id": 1,
    "question": "What is Django?",
    "answer": "<p>Django is a high-level Python web framework.</p>"
}
```
5. Delete an FAQ
Delete an existing FAQ by its ID.

Endpoint
DELETE /api/faqs/{id}/
Example Request
```bash
curl -X DELETE http://localhost:8000/api/faqs/1/
```
Response
Status Code: 204 No Content

Running Tests
To run the test suite, execute the following command:

```bash
docker-compose exec web python manage.py test
```
Technologies Used
Django

Django REST Framework

Redis (for caching)

Docker (for containerization)
