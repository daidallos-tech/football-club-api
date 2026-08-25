# ⚽️Football API

> REST API for a football application built with FastAPI.


## 📌 About the Project

This project was created as a learning and portfolio project to practice backend development with FastAPI. I've got feedback about my last project and decided to use it in this project. The most important part about creation this project for me was understand how pattern "Repository" works. I also tried to optimize DB and make it works fast. (I used CITEXT and b-tree)

---

## ✨ Features

### Authentication & Users

- User avatar upload
- User registration
- JWT authentication
- Password hashing
- Admin features (delete, update, create)

### Teams

- CRUD (for movie by admin)
- Pagination
- External API to fulfill your DB or update data

### Players

- CRUD (for director by admin)
- Pagination\
- External API to fulfill your DB or update data

### Additional Features

- Password reset via email
- Image upload and processing
- Database migrations
- External API to fulfill your DB or update data

---

## 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Backend language |
| FastAPI | Web framework |
| SQLAlchemy | ORM |
| PostgreSQL | Database |
| Alembic | Database migrations |
| Pydantic | Data validation |
| JWT | Authentication |
| Pytest | Testing |
| Docker | Containerization |

---

## 🏛️ Project Structure
<img width="574" height="1862" alt="image" src="https://github.com/user-attachments/assets/2dbecbd3-45e3-4745-9a9d-92a4661f709d" />

## 🔐 Authentication
I created two roles - admin and user. Both of them use JWT authentication.
I decided to make just one token for whole session and made this token alive for 30 days.

User
  │
  ▼
Login
  │
  ▼
Access Token
  │
  ▼
Authorization: Bearer (token)
  │
  ▼
Protected endpoint

## 🗄 Database
We have 6 tables in database. Also I use alembic for migrations.

1. User
2. Teams
3. Players -> (one-to-many with teams)
4. Password Reset -> (one-to-many with users)

## 📺 Endpoints screenshots.

User/Admin Endpoints ->
<img width="3150" height="1778" alt="image" src="https://github.com/user-attachments/assets/49cb39e3-cb67-4fb8-b909-fcad84c30135" />


Teams/Players Endpoints ->
<img width="3150" height="1548" alt="image" src="https://github.com/user-attachments/assets/ea83a347-5c99-4880-92f2-09fe09741ccd" />



## 🚀 How to install?

1. Clone repository 
```bash
git clone git@github.com:daidallos-tech/football-club-api.git
```
2. Go to project directory
```bash
cd football-club-api
```
3. Create .env file and copy everything from .env.example to paste in .env
4. Use docker command to start the project
```bash
docker compose up -d --build
```
5. For external API I used - https://www.football-data.org/pricing
6. Register, grab the token and past it in .env file.
7. To fulfill DATABASE.
```bash
docker compose exec -e PYTHONPATH=/src/football_club_api/src api uv run python src/football_club_api/main_sync.py
```


🧪 Testing

Tests are written using Pytest.

To run test (outside docker container)

```bash
python -m pytest -s -v
```
Tests screenshot
<img width="1886" height="254" alt="image" src="https://github.com/user-attachments/assets/e5954092-a6e9-4a43-a125-69ab59867808" />

