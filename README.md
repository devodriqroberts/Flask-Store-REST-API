
# REST API with Flask, Docker, Flask-Smorest, and Flask-SQLAlchemy

## Features

- **Flask**: Web framework for building the API
- **Flask-Smorest**: Simplifies API creation with built-in schema validation and error handling
- **Flask-SQLAlchemy**: Object-relational mapper (ORM) for managing database models
- **Docker**: For containerized development and deployment, ensuring a consistent environment across systems
- **TODO** **JWT Authentication**: Secure access to API endpoints with token-based authentication
- **TODO** **PostgreSQL/SQLite**: Database integration for structured data storage and retrieval

## Project Setup

### Prerequisites

- **Python 3.x**
- **Docker** installed
- **PostgreSQL** or **SQLite** (if using locally)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/devodriqroberts/Flask-Store-REST-API.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Flask-Store-REST-API
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables in a `.env` file:

   ```
   FLASK_APP=app
   FLASK_ENV=development
   SECRET_KEY=your-secret-key
   DATABASE_URL=postgresql://user:password@localhost:5432/dbname
   ```

### Running the Application

#### With Docker

1. Build and run the app:

   ```bash
   docker-compose up --build
   ```

2. The API will be accessible at:

   ```
   http://localhost:5000
   ```

#### Without Docker

1. Initialize the database:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

2. Run the application:

   ```bash
   flask run
   ```

### API Endpoints

- **POST** `/register`: Register a new user
- **POST** `/login`: Authenticate and retrieve a JWT token
- **GET** `/resource`: Access protected resources (JWT required)
- **CRUD Operations** for managing various resources

### Testing

Run tests to ensure the application is working as expected:

```bash
pytest
```

## Acknowledgments

This project is based on the **"Build Professional REST APIs with Python, Flask, Docker, Flask-Smorest, and Flask-SQLAlchemy"** course by Jose.

## License

This project is licensed under the MIT License.
