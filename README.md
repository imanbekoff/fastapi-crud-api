\# FastAPI CRUD API



A REST API built with Python, FastAPI, SQLAlchemy, and PostgreSQL.



\## Features



\- Create users

\- Retrieve users by ID

\- Update user information

\- Delete users

\- Validate input data with Pydantic

\- Handle duplicate emails

\- Manage database transactions

\- Test API endpoints with pytest



\## Tech Stack



\- Python

\- FastAPI

\- SQLAlchemy

\- PostgreSQL

\- Pydantic

\- Pytest



\## Setup



\### 1. Clone the repository



git clone https://github.com/imanbekoff/fastapi-crud-api.git

cd fastapi-crud-api



\### 2. Create a virtual environment



python -m venv .venv



Activate it on Windows:

.venv\\Scripts\\activate



\### 3. Install dependencies



python -m pip install -r requirements.txt



\### 4. Configure environment variables



Create a `.env` file in the project root:

DB\_PASSWORD=your\_postgresql\_password



Update the PostgreSQL connection settings in `db\_orm.py` if needed. Create a database named `learning\_db` before starting the API.



\### 5. Run the API



uvicorn main:app --reload



Open the interactive API documentation:



http://127.0.0.1:8000/docs



\## Run Tests



python -m pytest -v

