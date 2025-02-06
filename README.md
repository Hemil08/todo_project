# Django To-Do App

A collaborative To-Do application built using Django and Jinja templates, allowing users to create tasks, invite team members, manage subtasks, and track progress efficiently.

## Features

- **User Authentication:** Sign up, log in, and log out functionality.
- **Task Management:** Users can create, update, and delete tasks.
- **Team Collaboration:** Invite other users to work on shared tasks.
- **Subtasks:** Break down larger tasks into smaller, manageable subtasks.
- **Task Assignment:** Assign tasks and subtasks to specific team members.
- **Comment Tasks:** Users can also add comments in tasks.

## Installation

### Prerequisites
Ensure you have the following installed:
- Python 3.x
- Django
- Git
- Virtual Environment (optional but recommended)

### Setup Steps
1. **Clone the repository:**
   ```sh
   git clone https://github.com/Hemil08/todo_project.git
   cd todo_project
   ```

2. **Create a virtual environment (optional but recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply database migrations:**
   ```sh
   python manage.py migrate
   ```

5. **Create a superuser (for admin access):**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the development server:**
   ```sh
   python manage.py runserver
   ```
   The app should now be accessible at `http://127.0.0.1:8000/`

## Usage

1. **Sign up/Login**
   - Create an account or log in to access the dashboard.

2. **Create a Task**
   - Add a new task with a title, description, and deadline.

3. **Invite Team Members**
   - Share tasks with team members via invitations.

4. **Manage Subtasks**
   - Add, edit, or complete subtasks under a parent task.

5. **Track Progress**
   - View updates and commit history to monitor team contributions.

## Technologies Used
- **Backend:** Django (Python)
- **Frontend:** Jinja (Django templates), HTML, CSS, JavaScript
- **Database:** SQLite (default), can be configured for PostgreSQL/MySQL
- **Authentication:** Django Auth System

## Contribution Guidelines
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes and push to your forked repo.
4. Create a pull request.

## License
This project is open-source and available under the MIT License.

## Contact
For questions or suggestions, reach out at [your email/contact info].

