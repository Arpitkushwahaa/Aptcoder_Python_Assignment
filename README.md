# EdTech NLP-to-SQL API

An AI-powered backend service that converts natural language questions into SQL queries and returns answers from an EdTech database.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Setup Instructions](#setup-instructions)
- [API Documentation](#api-documentation)
- [NLP-to-SQL Approach](#nlp-to-sql-approach)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Limitations](#limitations)
- [Project Structure](#project-structure)

## Overview

This project implements an intelligent backend service for an EdTech platform that allows non-technical users to query educational data using natural language. The system uses Google's Gemini AI model to convert questions like "How many students enrolled in Python courses in 2024?" into valid SQL queries and executes them safely.

## Features

- ✅ Natural language to SQL conversion using LLM (Google Gemini AI)
- ✅ Safe SQL execution with query validation (only SELECT queries allowed)
- ✅ RESTful API built with FastAPI
- ✅ Analytics endpoint for query statistics
- ✅ Comprehensive test suite with pytest
- ✅ Docker containerization
- ✅ Kubernetes deployment configuration
- ✅ SQLite database with seeded data
- ✅ Query logging and performance tracking

## Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│      FastAPI Application        │
│  ┌───────────────────────────┐  │
│  │  POST /query              │  │
│  │  GET /stats               │  │
│  │  GET /health              │  │
│  └───────────────────────────┘  │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│    NLP-to-SQL Service           │
│    (Google Gemini AI)           │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│    SQL Executor                 │
│    - Query Validation           │
│    - Safe Execution             │
│    - Result Processing          │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│    SQLite Database              │
│    - students                   │
│    - courses                    │
│    - enrollments                │
│    - query_logs                 │
└─────────────────────────────────┘
```

## Setup Instructions

### Prerequisites

- Python 3.11 or higher
- Google Gemini API key
- pip (Python package manager)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Aptcoder_python_Assignment
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   # Copy the example file
   copy .env.example .env
   
   # Edit .env and add your Gemini API key
   GEMINI_API_KEY=your-actual-api-key-here
   DATABASE_URL=sqlite:///./edtech.db
   ```

5. **Initialize and seed the database**
   ```bash
   python -m app.seed
   ```

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

7. **Access the API**
   - API: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

## API Documentation

### POST /query

Convert natural language question to SQL and execute it.

**Request:**
```json
{
  "question": "How many students enrolled in Python courses in 2024?"
}
```

**Response:**
```json
{
  "question": "How many students enrolled in Python courses in 2024?",
  "generated_sql": "SELECT COUNT(DISTINCT e.student_id) FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.name LIKE '%Python%' AND strftime('%Y', e.enrolled_at) = '2024'",
  "result": 5,
  "execution_time_ms": 45
}
```

### GET /stats

Get analytics about executed queries.

**Response:**
```json
{
  "total_queries": 10,
  "most_common_keywords": [
    {"keyword": "students", "count": 5},
    {"keyword": "enrolled", "count": 4},
    {"keyword": "courses", "count": 3}
  ],
  "slowest_query": {
    "question": "List all students with their courses",
    "generated_sql": "SELECT s.name, c.name FROM students s JOIN enrollments e ON s.id = e.student_id JOIN courses c ON e.course_id = c.id",
    "execution_time_ms": 150,
    "created_at": "2024-01-20T10:30:00"
  }
}
```

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Example Queries

Here are some example questions you can ask:

1. **Count queries:**
   - "How many students are enrolled?"
   - "How many courses are available?"
   - "How many students enrolled in Python courses in 2024?"

2. **List queries:**
   - "List all students"
   - "Show me all courses in the Programming category"
   - "List students enrolled in Data Science"

3. **Analytical queries:**
   - "Which course has the most enrollments?"
   - "Show me students in grade 10"
   - "What courses did Alice Johnson enroll in?"

## NLP-to-SQL Approach

### LLM-Based Approach (Google Gemini AI)

This implementation uses an **LLM-based approach** for converting natural language to SQL, which is the preferred method for this assignment.

#### How It Works

1. **Schema Context:** The system provides the database schema to the LLM:
   - Table structures (students, courses, enrollments)
   - Column names and types
   - Relationships between tables

2. **Prompt Engineering:** A carefully crafted system prompt instructs the LLM to:
   - Generate only SELECT queries
   - Use proper SQLite syntax
   - Apply appropriate JOINs
   - Handle date/time filtering
   - Return clean SQL without markdown formatting

3. **Query Generation:** The LLM processes the natural language question along with the schema context to generate an appropriate SQL query.

4. **Validation:** Before execution, the generated SQL is validated to ensure:
   - It starts with SELECT
   - No forbidden keywords (DELETE, DROP, UPDATE, INSERT, etc.)
   - Proper syntax

#### Advantages

- **Flexibility:** Handles complex, varied natural language queries
- **Context Awareness:** Understands relationships between tables
- **Natural Language Understanding:** Interprets user intent accurately
- **Minimal Maintenance:** No need for extensive rule definitions

#### Safety Measures

1. **Query Validation:** Multi-layer validation prevents malicious queries
2. **Keyword Blocking:** Hardcoded blocks for dangerous SQL operations
3. **SELECT-Only Policy:** Only read operations are permitted
4. **Error Handling:** Comprehensive error messages for invalid queries

### Alternative: Rule-Based Approach

While not implemented, a rule-based approach could use:
- Pattern matching with regex
- Keyword extraction
- Template-based SQL generation
- Limited to predefined query patterns

**Why LLM is Better:**
- More flexible and adaptable
- Handles complex queries
- Better understanding of context
- Less maintenance overhead

## Testing

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=app --cov-report=html
```

### Run Specific Test File

```bash
pytest tests/test_nlp2sql.py
pytest tests/test_api.py
```

### Test Coverage

The test suite includes:

1. **NLP-to-SQL Tests** (`test_nlp2sql.py`)
   - Query validation
   - Forbidden keyword blocking
   - Schema information verification

2. **SQL Executor Tests** (`test_sql_executor.py`)
   - Query execution
   - Result processing
   - Error handling

3. **Analytics Tests** (`test_analytics.py`)
   - Statistics calculation
   - Keyword extraction
   - Slowest query tracking

4. **API Tests** (`test_api.py`)
   - Endpoint functionality
   - Input validation
   - Response structure

## Docker Deployment

### Build Image

```bash
docker build -t edtech-nlp2sql:latest .
```

### Run Container

```bash
docker run -d \
  --name edtech-api \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your-api-key-here" \
  edtech-nlp2sql:latest
```

### View Logs

```bash
docker logs -f edtech-api
```

### Stop Container

```bash
docker stop edtech-api
docker rm edtech-api
```

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (minikube, kind, or cloud provider)
- kubectl configured

### Deploy to Kubernetes

1. **Create secret with API key:**
   ```bash
   # Edit k8s-secret.yaml and add your API key
   kubectl apply -f k8s-secret.yaml
   ```

2. **Deploy the pod:**
   ```bash
   kubectl apply -f k8s-pod.yaml
   ```

3. **Create the service:**
   ```bash
   kubectl apply -f k8s-service.yaml
   ```

4. **Check deployment:**
   ```bash
   kubectl get pods
   kubectl get services
   ```

5. **Access the application:**
   ```bash
   # Port forward to local machine
   kubectl port-forward edtech-nlp2sql-pod 8000:8000
   ```

### Resource Limits

The Kubernetes pod is configured with:

- **Memory:**
  - Request: 256Mi
  - Limit: 512Mi

- **CPU:**
  - Request: 250m (0.25 cores)
  - Limit: 500m (0.5 cores)

### Health Checks

- **Liveness Probe:** Checks if the application is running
- **Readiness Probe:** Checks if the application is ready to serve traffic

## Limitations

### Current Limitations

1. **LLM Dependency:**
   - Requires Google Gemini API key
   - API calls (free tier available)
   - Network latency for API calls

2. **Query Accuracy:**
   - LLM may occasionally generate incorrect SQL
   - Complex queries might need refinement
   - Depends on quality of natural language input

3. **Database:**
   - SQLite is not suitable for production high-traffic scenarios
   - No concurrent write support
   - Limited to single file

4. **Security:**
   - No user authentication/authorization
   - API key stored in environment variables
   - No rate limiting implemented

5. **Scalability:**
   - Single instance design
   - Database file storage limits horizontal scaling
   - No caching mechanism

### Potential Improvements

1. **Database:**
   - Migrate to PostgreSQL for production
   - Implement connection pooling
   - Add database migrations (Alembic)

2. **Performance:**
   - Implement query result caching
   - Add rate limiting
   - Optimize SQL queries

3. **Security:**
   - Add JWT authentication
   - Implement role-based access control
   - Use secrets management (Vault, AWS Secrets Manager)

4. **Monitoring:**
   - Add logging with structured logs
   - Implement metrics (Prometheus)
   - Add distributed tracing

5. **Features:**
   - Query suggestions
   - Query history for users
   - Export results to CSV/Excel
   - Visualization of results

## Project Structure

```
Aptcoder_python_Assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── nlp2sql.py           # NLP-to-SQL service
│   ├── sql_executor.py      # SQL execution service
│   ├── analytics.py         # Analytics service
│   └── seed.py              # Database seeding
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test configuration
│   ├── test_nlp2sql.py      # NLP-to-SQL tests
│   ├── test_sql_executor.py # SQL executor tests
│   ├── test_analytics.py    # Analytics tests
│   └── test_api.py          # API endpoint tests
│
├── Dockerfile               # Docker configuration
├── k8s-pod.yaml            # Kubernetes pod definition
├── k8s-service.yaml        # Kubernetes service definition
├── k8s-secret.yaml         # Kubernetes secret template
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Database Schema

### students
| Column     | Type     | Description          |
|------------|----------|----------------------|
| id         | INTEGER  | Primary key          |
| name       | VARCHAR  | Student name         |
| grade      | INTEGER  | Grade level (9-12)   |
| created_at | DATETIME | Registration date    |

### courses
| Column   | Type    | Description              |
|----------|---------|--------------------------|
| id       | INTEGER | Primary key              |
| name     | VARCHAR | Course name              |
| category | VARCHAR | Course category          |

### enrollments
| Column      | Type     | Description                    |
|-------------|----------|--------------------------------|
| id          | INTEGER  | Primary key                    |
| student_id  | INTEGER  | Foreign key to students.id     |
| course_id   | INTEGER  | Foreign key to courses.id      |
| enrolled_at | DATETIME | Enrollment date                |

### query_logs
| Column         | Type     | Description                |
|----------------|----------|----------------------------|
| id             | INTEGER  | Primary key                |
| question       | VARCHAR  | Natural language question  |
| generated_sql  | VARCHAR  | Generated SQL query        |
| execution_time | INTEGER  | Execution time (ms)        |
| created_at     | DATETIME | Query timestamp            |

## Technologies Used

- **FastAPI:** Modern Python web framework
- **SQLAlchemy:** SQL toolkit and ORM
- **Pydantic:** Data validation using Python type hints
- **Google Gemini AI:** LLM for NLP-to-SQL conversion
- **SQLite:** Lightweight database
- **pytest:** Testing framework
- **Docker:** Containerization
- **Kubernetes:** Container orchestration
- **Uvicorn:** ASGI server

## Contributing

This is an assignment project. For the actual repository, follow these guidelines:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests
5. Submit a pull request

## License

This project is created as part of a technical assignment.

## Support

For questions or issues, please contact the development team or create an issue in the repository.

---

**Built with ❤️ for EdTech**
