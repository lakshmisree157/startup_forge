# Connection Management API

A FastAPI-based application for managing connection requests between users, specifically designed for founders and investors in a networking platform.

## Features

- Send connection requests between users
- Accept or reject incoming connection requests
- Retrieve list of connections for a user
- Database health check endpoint
- RESTful API with proper error handling
- PostgreSQL database integration
- Pydantic models for data validation

## Prerequisites

- Python 3.8+
- PostgreSQL database
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install fastapi uvicorn psycopg2-binary python-dotenv
   ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
```

## Database Setup

1. Ensure PostgreSQL is running and create a database.

2. Create the required tables:

```sql
-- Connection Requests Table
CREATE TABLE connection_requests (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER NOT NULL,
    sender_role VARCHAR(50) NOT NULL,
    receiver_id INTEGER NOT NULL,
    receiver_role VARCHAR(50) NOT NULL,
    message TEXT,
    status VARCHAR(20) DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP
);

-- Connections Table
CREATE TABLE connections (
    id SERIAL PRIMARY KEY,
    user_a_id INTEGER NOT NULL,
    user_a_role VARCHAR(50) NOT NULL,
    user_b_id INTEGER NOT NULL,
    user_b_role VARCHAR(50) NOT NULL,
    connection_request_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (connection_request_id) REFERENCES connection_requests(id)
);
```

## Running the Application

1. Ensure your `.env` file is configured with correct database credentials.

2. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

3. The API will be available at `http://localhost:8000`

4. Interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### Health Check
- `GET /health/db` - Check database connection

### Connection Requests
- `POST /api/connections/request` - Send a connection request
- `GET /api/connections/requests/incoming` - Get incoming connection requests
- `PUT /api/connections/requests/{request_id}/accept` - Accept a connection request
- `PUT /api/connections/requests/{request_id}/reject` - Reject a connection request

### Connections
- `GET /api/connections` - Get user's connections

## Testing with Postman

Import the `postman_collection.json` file into Postman to test the API endpoints. The collection includes pre-configured requests for all available endpoints.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.
