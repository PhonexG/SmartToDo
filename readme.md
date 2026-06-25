# SmartToDo

SmartToDo is a simple task manager built with Django.
The main idea of the project is to create tasks, track their status, group them by topics, and estimate how risky they are based on deadline and difficulty.

I made this project mostly to practice Django, Docker, MySQL, user authentication, and basic AI integration.

## Features

* User registration and login
* Create, edit, and delete tasks
* Change task status without editing the whole task
* Filter tasks by status, risk, and overdue state
* Dashboard with task statistics
* Automatic topic grouping for tasks
* Completion chance and risk level calculation
* Simple responsive frontend
* Docker setup with MySQL

## Tech stack

* Python
* Django
* MySQL
* Docker / Docker Compose
* HTML / CSS
* Local AI model for topic grouping

## How to run

Clone the repository:

```bash
git clone <your-repository-url>
cd SmartToDo
```

Create a `.env` file in the project root:

```env
SECRET_KEY=your_secret_key
DEBUG=True

MYSQL_DATABASE=smart_todo
MYSQL_USER=smart_user
MYSQL_PASSWORD=smart_password
MYSQL_ROOT_PASSWORD=root_password
MYSQL_HOST=db
MYSQL_PORT=3306
```

Run the project with Docker:

```bash
docker compose up --build
```

Apply migrations:

```bash
docker compose exec web python manage.py migrate
```

Create admin user if needed:

```bash
docker compose exec web python manage.py createsuperuser
```

Open the app:

```text
http://127.0.0.1:8000/
```

## Project structure

```text
SmartToDo/
├── accounts/
├── ai_tools/
├── dashboard/
├── tasks/
├── config/
├── templates/
├── static/
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Notes

The project is not supposed to be a big production app.
It is a learning project where I tried to connect normal Django CRUD logic with some simple AI-related features.

## Possible future improvements

* Better AI topic grouping
* More detailed task priority system
* Search by task title and description
* Better mobile layout
* Task reminders
* Dark/light theme switch
