# fitness-database-blg317

A comprehensive Gym Management System API built with Flask and PostgreSQL.

## Project Setup Instructions

This guide provides step-by-step instructions to set up and run the Gym Management API project.

### Prerequisites

Ensure you have the following installed on your system:
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/)

### Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository_url>
    cd fitness-database-blg317
    ```

2.  **Create a Virtual Environment**:
    It's recommended to use a virtual environment to manage dependencies.
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

1.  **Create the Database**:
    Access your PostgreSQL terminal (psql) or use a tool like pgAdmin.
    ```sql
    CREATE DATABASE fitness_db;
    ```

2.  **Create Database User**:
    The default configuration uses the user `postgres` with password `12345`. You can create a specific user or use your existing one.
    ```sql
    -- Optional: Create a dedicated user
    CREATE USER myuser WITH PASSWORD 'mypassword';
    GRANT ALL PRIVILEGES ON DATABASE fitness_db TO myuser;
    ```

3.  **Seed the Database**:
    Run the `seed_data.sql` script to create tables and insert initial data.
    ```bash
    psql -U postgres -d fitness_db -f seed_data.sql
    ```
    *Note: Replace `postgres` with your database username if different.*

### Configuration

1.  **Configure Database Connection**:
    Open `config.py` and update the database connection details if they differ from the defaults.
    ```python
    class Config:
        DB_HOST = "localhost"
        DB_NAME = "fitness_db"
        DB_USER = "postgres"  # Change to your DB user
        DB_PASS = "12345"     # Change to your DB password
    ```

2.  **Environment Variables**:
    You can also set environment variables for sensitive keys.
    - `SECRET_KEY`: Flask secret key
    - `JWT_SECRET_KEY`: JWT secret key

## Running the Application

1.  **Start the Flask Application**:
    ```bash
    python run.py
    ```

2.  **Access the API**:
    The application will start at `http://127.0.0.1:5001/`.

3.  **API Documentation (Swagger)**:
    Visit `http://127.0.0.1:5001/apidocs/` to explore and test the API endpoints using Swagger UI.
