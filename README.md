# Project Management API

This Django project provides a RESTful API for managing projects, tasks, and users.

## Features

1. **User Authentication**: Utilizes JWT (JSON Web Token) authentication for user authentication and authorization.
2. **Project Management**: Users can create projects and add multiple users to their projects. Each project has a unique name and description.
3. **Task Management**: Within each project, users can perform CRUD (Create, Read, Update, Delete) operations on tasks. Each task has a title, description, status, and due date.
4. **Soft Delete**: Implements soft delete functionality for both projects and tasks. Soft delete means marking records as deleted instead of physically removing them from the database.

## API Endpoints

### Authentication

- `/api/token/`: POST request to obtain JWT token for authentication.
- `/api/refresh/token`: POST request to refresh expired JWT token for authentication.

### Users

- `/api/register/`: POST request to register a new user.

### Projects

- `/api/projects/`: GET request to retrieve all projects. POST request to create a new project.
- `/api/projects/<project_id>/`: GET, PUT, DELETE requests to retrieve, update, or delete a specific project.
- `/api/projects/<project_id>/add_member/`: POST request to add a member to a project.

### Tasks

- `/api/projects/<project_id>/tasks/`: GET request to retrieve all tasks within a project. POST request to create a new task within a project.
- `/api/projects/<project_id>/tasks/<task_id>/`: GET, PUT, DELETE requests to retrieve, update, or delete a specific task within a project.

### Soft Delete

- `/api/projects/<project_id>/undelete/`: POST request to undelete a project.
- `/api/projects/<project_id>/tasks/<task_id>/undelete/`: POST request to undelete a task within a project.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/tabish-siraj/project-management-api.git
