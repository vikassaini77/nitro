File Parser CRUD API with Progress Tracking
This project is a backend application that supports uploading, storing, parsing, and retrieving files, with real-time progress tracking for large uploads. The solution is built with FastAPI, Celery, and PostgreSQL, and is fully containerized with Docker for easy setup and deployment.

✨ Features
File Upload: Upload large files via a multipart form-data request.

Asynchronous Parsing: File parsing is handled in the background by a Celery worker to prevent blocking the API.

Real-time Progress Tracking: Get the current status and progress percentage of a file upload and parsing process.

CRUD Operations: List all uploaded files and delete specific files.

Data Persistence: File metadata and parsed content are stored in a PostgreSQL database.

Authentication: API endpoints are protected using JWT bearer tokens.

Interactive Documentation: Automatic, interactive API documentation provided by FastAPI at the /docs endpoint.

Bonus Features: Includes WebSocket and Server-Sent Events (SSE) for real-time progress updates.

🛠️ Tech Stack
Backend: Python, FastAPI

Database: PostgreSQL

Asynchronous Tasks: Celery, Redis

Containerization: Docker, Docker Compose

Libraries: SQLAlchemy, Pydantic, Passlib, python-jose

🚀 Getting Started
Prerequisites
Docker installed on your machine.

Setup Instructions
Clone the repository:

git clone <your-repository-url>
cd <your-repository-name>

Create an environment file:
Copy the .env.example file to a new file named .env. The default values are already configured to work with Docker Compose.

cp .env.example .env

Build and run the application:
Use Docker Compose to build the images and start all the services (API, worker, database, and Redis).

docker-compose up --build

The API will be available at http://localhost:8000.

📚 API Documentation
For a full, interactive API documentation, please run the application and navigate to:
http://localhost:8000/docs

Authentication
First, obtain an authentication token by sending your credentials to the /auth/token endpoint.

Endpoint: POST /auth/token

Request Body: application/x-www-form-urlencoded

username: admin

password: admin123

Success Response (200 OK):

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}

Then, click the "Authorize" button in the Swagger UI and enter bearer <your_token> to access the protected endpoints.

Main Endpoints
Method

Endpoint

Description

POST

/files

Upload a new file for processing.

GET

/files

List all uploaded files and their status.

GET

/files/{file_id}

Get the parsed content of a specific file.

GET

/files/{file_id}/progress

Get the current progress of a file.

DELETE

/files/{file_id}

Delete a file and its parsed content.

Sample Request: Upload File
Endpoint: POST /files

Request Body: multipart/form-data

file: (your file, e.g., data.csv)

Success Response (201 Created):

{
  "file_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "uploading",
  "progress": 0
}

Sample Response: Get Progress
Endpoint: GET /files/{file_id}/progress

Success Response (200 OK):

{
  "file_id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
  "status": "processing",
  "progress": 75
}
---

## 🧪 Testing with cURL

Here are some sample `cURL` commands to test the API from your terminal.

1.  **Get Authentication Token**
    (Replace `admin` and `admin123` if you changed the demo credentials)

    ```bash
    curl -X POST "http://localhost:8000/auth/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin&password=admin123"
    ```

2.  **List All Files**
    (Replace `<YOUR_TOKEN>` with the access token you received from the login command)

    ```bash
    curl -X GET "http://localhost:8000/files" \
    -H "Authorization: Bearer <YOUR_TOKEN>"
    ```

3.  **Upload a File**
    (Replace `<YOUR_TOKEN>` and `<PATH_TO_YOUR_FILE>` with your actual token and a path to a test file on your computer)

    ```bash
    curl -X POST "http://localhost:8000/files" \
    -H "Authorization: Bearer <YOUR_TOKEN>" \
    -F "file=@<PATH_TO_YOUR_FILE>"
    ```

4.  **Check File Progress**
    (Replace `<YOUR_TOKEN>` and `<FILE_ID>` with your token and the file ID from the upload response)

    ```bash
    curl -X GET "http://localhost:8000/files/<FILE_ID>/progress" \
    -H "Authorization: Bearer <YOUR_TOKEN>"
    