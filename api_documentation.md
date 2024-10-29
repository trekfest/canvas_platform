# API Documentation

## Authentication

### Register User
- **URL:** `/api/v1/auth/registration/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "username": "username",
      "first_name": "First Name",
      "last_name": "Last Name",
      "password1": "password",
      "password2": "password"
    }
    ```

### Login User
- **URL:** `/api/v1/auth/login/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "email": "user@example.com",
      "password": "password"
    }
    ```

### Google Login
- **URL:** `/api/v1/auth/google/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "access_token": "google_access_token"
    }
    ```

### Google Login Callback
- **URL:** `/api/v1/auth/google/callback/`
- **Method:** `GET`
- **Description:** Callback endpoint after successful Google login.

### Logout User
- **URL:** `/api/v1/auth/logout/`
- **Method:** `POST`

## Users

### Get User Profile
- **URL:** `/api/users/me/`
- **Method:** `GET`

### Update User Profile
- **URL:** `/api/users/me/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "username": "new_username",
      "first_name": "New First Name",
      "last_name": "New Last Name"
    }
    ```

## Courses

### List Courses
- **URL:** `/api/courses/`
- **Method:** `GET`

### Create Course
- **URL:** `/api/courses/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "course_name": "Course Name",
      "course_code": "COURSE123",
      "description": "Course description",
      "credits": 3,
      "teacher": "teacher_user_id"
    }
    ```

### Retrieve Course
- **URL:** `/api/courses/{course_id}/`
- **Method:** `GET`

### Update Course
- **URL:** `/api/courses/{course_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "course_name": "Updated Course Name",
      "course_code": "UPDATEDCODE",
      "description": "Updated description",
      "credits": 4,
      "teacher": "updated_teacher_user_id"
    }
    ```

### Delete Course
- **URL:** `/api/courses/{course_id}/`
- **Method:** `DELETE`

## Enrollments

### List Enrollments
- **URL:** `/api/enrollments/`
- **Method:** `GET`

### Enroll in Course
- **URL:** `/api/enrollments/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "student": "student_user_id",
      "course": "course_id",
      "enrollment_date": "YYYY-MM-DD"
    }
    ```

### Retrieve Enrollment
- **URL:** `/api/enrollments/{enrollment_id}/`
- **Method:** `GET`

### Update Enrollment
- **URL:** `/api/enrollments/{enrollment_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "grade": "A"
    }
    ```

### Delete Enrollment
- **URL:** `/api/enrollments/{enrollment_id}/`
- **Method:** `DELETE`

## Assignments

### List Assignments
- **URL:** `/api/assignments/`
- **Method:** `GET`

### Create Assignment
- **URL:** `/api/assignments/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "course": "course_id",
      "title": "Assignment Title",
      "description": "Assignment Description",
      "due_date": "YYYY-MM-DDTHH:MM:SSZ"
    }
    ```

### Retrieve Assignment
- **URL:** `/api/assignments/{assignment_id}/`
- **Method:** `GET`

### Update Assignment
- **URL:** `/api/assignments/{assignment_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "title": "Updated Title",
      "description": "Updated Description",
      "due_date": "YYYY-MM-DDTHH:MM:SSZ"
    }
    ```

### Delete Assignment
- **URL:** `/api/assignments/{assignment_id}/`
- **Method:** `DELETE`

## Submissions

### List Submissions
- **URL:** `/api/submissions/`
- **Method:** `GET`

### Submit Assignment
- **URL:** `/api/submissions/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "assignment": "assignment_id",
      "student": "student_user_id",
      "grade": "A",
      "feedback": "Good job!"
    }
    ```

### Retrieve Submission
- **URL:** `/api/submissions/{submission_id}/`
- **Method:** `GET`

### Update Submission
- **URL:** `/api/submissions/{submission_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "grade": "B",
      "feedback": "Needs improvement."
    }
    ```

### Delete Submission
- **URL:** `/api/submissions/{submission_id}/`
- **Method:** `DELETE`

## Materials

### List Materials
- **URL:** `/api/materials/`
- **Method:** `GET`

### Upload Material
- **URL:** `/api/materials/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "course": "course_id",
      "title": "Material Title",
      "description": "Material Description",
      "file_path": "path/to/file"
    }
    ```

### Retrieve Material
- **URL:** `/api/materials/{material_id}/`
- **Method:** `GET`

### Update Material
- **URL:** `/api/materials/{material_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "title": "Updated Title",
      "description": "Updated Description"
    }
    ```

### Delete Material
- **URL:** `/api/materials/{material_id}/`
- **Method:** `DELETE`

## Schedules

### List Schedules
- **URL:** `/api/schedules/`
- **Method:** `GET`

### Create Schedule
- **URL:** `/api/schedules/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "course": "course_id",
      "start_time": "YYYY-MM-DDTHH:MM:SSZ",
      "end_time": "YYYY-MM-DDTHH:MM:SSZ",
      "day_of_week": "Monday"
    }
    ```

### Retrieve Schedule
- **URL:** `/api/schedules/{schedule_id}/`
- **Method:** `GET`

### Update Schedule
- **URL:** `/api/schedules/{schedule_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "start_time": "YYYY-MM-DDTHH:MM:SSZ",
      "end_time": "YYYY-MM-DDTHH:MM:SSZ"
    }
    ```

### Delete Schedule
- **URL:** `/api/schedules/{schedule_id}/`
- **Method:** `DELETE`

## Calendar

### List Calendar Events
- **URL:** `/api/calendar/`
- **Method:** `GET`

### Create Calendar Event
- **URL:** `/api/calendar/`
- **Method:** `POST`
- **Request Body:**
    ```json
    {
      "student": "student_user_id",
      "course": "course_id",
      "event_type": "Assignment",
      "title": "Event Title",
      "description": "Event Description",
      "due_date": "YYYY-MM-DDTHH:MM:SSZ"
    }
    ```

### Retrieve Calendar Event
- **URL:** `/api/calendar/{event_id}/`
- **Method:** `GET`

### Update Calendar Event
- **URL:** `/api/calendar/{event_id}/`
- **Method:** `PUT`
- **Request Body:**
    ```json
    {
      "title": "Updated Title",
      "description": "Updated Description"
    }
    ```

### Delete Calendar Event
- **URL:** `/api/calendar/{event_id}/`
- **Method:** `DELETE`