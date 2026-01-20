# Getting Started Guide

This guide will walk you through setting up and running the EdTech NLP-to-SQL API.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.11+** installed
   - Check: `python --version`
   - Download from: https://www.python.org/downloads/

2. **Google Gemini API Key**
   - Sign up at: https://aistudio.google.com/
   - Create an API key from your account dashboard
   - **Important:** You'll need this for the application to work

3. **Git** (optional, for cloning)
   - Check: `git --version`
   - Download from: https://git-scm.com/

## Quick Start (Automated)

### Windows
```bash
# Run the automated setup script
setup.bat

# Edit .env file with your Gemini API key
notepad .env

# Start the application
uvicorn app.main:app --reload
```

### Linux/Mac
```bash
# Make the script executable
chmod +x setup.sh

# Run the automated setup script
./setup.sh

# Edit .env file with your Gemini API key
nano .env

# Start the application
uvicorn app.main:app --reload
```

## Manual Setup (Step by Step)

### Step 1: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate

# Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

```bash
# Copy the example environment file
# Windows:
copy .env.example .env

# Linux/Mac:
cp .env.example .env

# Edit .env and add your Gemini API key
# The file should look like:
GEMINI_API_KEY=your-actual-api-key-here
DATABASE_URL=sqlite:///./edtech.db
```

### Step 4: Initialize Database

```bash
python -m app.seed
```

Expected output:
```
Initializing database...
Seeding data...
Database seeded successfully!
Created 12 students
Created 5 courses
Created 21 enrollments
```

### Step 5: Run the Application

```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [...]
INFO:     Started server process [...]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 6: Test the API

Open your browser and visit:
- **Interactive Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

## Testing the API

### Using the Interactive Docs (Recommended for Beginners)

1. Go to http://localhost:8000/docs
2. Click on **POST /query**
3. Click **Try it out**
4. Enter a question in the request body:
   ```json
   {
     "question": "How many students are enrolled?"
   }
   ```
5. Click **Execute**
6. View the response below

### Using cURL

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many students enrolled in Python courses in 2024?"}'
```

### Using Python Script

```bash
python example_usage.py
```

### Using PowerShell (Windows)

```powershell
$body = @{
    question = "How many students are enrolled?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/query" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_nlp2sql.py

# Run with coverage
pytest --cov=app --cov-report=html
```

## Docker Setup

### Build and Run with Docker

```bash
# Build the image
docker build -t edtech-nlp2sql:latest .

# Run the container
docker run -d \
  --name edtech-api \
  -p 8000:8000 \
  -e GEMINI_API_KEY="your-api-key-here" \
  edtech-nlp2sql:latest

# View logs
docker logs -f edtech-api

# Test the API
curl http://localhost:8000/health
```

### Stop and Remove Container

```bash
docker stop edtech-api
docker rm edtech-api
```

## Kubernetes Setup

### Prerequisites
- kubectl installed
- Kubernetes cluster running (minikube, kind, or cloud provider)

### Deploy to Kubernetes

```bash
# 1. Edit the secret with your API key
# Edit k8s-secret.yaml and replace 'your-gemini-api-key-here'

# 2. Apply the secret
kubectl apply -f k8s-secret.yaml

# 3. Deploy the pod
kubectl apply -f k8s-pod.yaml

# 4. Create the service
kubectl apply -f k8s-service.yaml

# 5. Check status
kubectl get pods
kubectl get services

# 6. Port forward to access locally
kubectl port-forward edtech-nlp2sql-pod 8000:8000

# 7. Test the API
curl http://localhost:8000/health
```

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### Issue: "Gemini API Key not found"

**Solution:** Ensure your `.env` file exists and contains the API key:
```bash
# Check if .env exists
# Windows:
type .env

# Linux/Mac:
cat .env

# It should contain:
GEMINI_API_KEY=your-actual-key
DATABASE_URL=sqlite:///./edtech.db
```

### Issue: "Database not found"

**Solution:** Initialize the database:
```bash
python -m app.seed
```

### Issue: "Port 8000 already in use"

**Solution:** Either stop the other process or use a different port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Issue: "Tests failing"

**Solution:** Make sure you're in the project root and the test database can be created:
```bash
# Make sure you're in the project root
cd Aptcoder_python_Assignment

# Run tests
pytest -v
```

## Example Questions to Try

Once the API is running, try these questions:

### Count Queries
- "How many students are enrolled?"
- "How many courses are available?"
- "How many students enrolled in Python courses in 2024?"
- "What is the total number of enrollments?"

### List Queries
- "List all students"
- "Show me all courses"
- "List students in grade 10"
- "Show courses in the Programming category"

### Analytical Queries
- "Which course has the most enrollments?"
- "What courses did Alice Johnson enroll in?"
- "Show students who enrolled in 2024"
- "List all enrollments for Python Programming"

## Next Steps

1. **Explore the API:** Try different questions in the interactive docs
2. **Check Analytics:** Visit http://localhost:8000/stats to see query statistics
3. **Run Tests:** Execute `pytest` to see all tests pass
4. **Deploy:** Try deploying with Docker or Kubernetes
5. **Customize:** Modify the code to add new features

## Project Structure Overview

```
Aptcoder_python_Assignment/
├── app/                    # Main application code
│   ├── main.py            # FastAPI application
│   ├── nlp2sql.py         # LLM-based NLP-to-SQL
│   ├── sql_executor.py    # Safe SQL execution
│   └── ...
├── tests/                  # Test suite
├── Dockerfile             # Docker configuration
├── k8s-*.yaml             # Kubernetes configs
├── README.md              # Full documentation
└── requirements.txt       # Dependencies
```

## Getting Help

- **Full Documentation:** See [README.md](README.md)
- **API Examples:** See [API_EXAMPLES.md](API_EXAMPLES.md)
- **Submission Checklist:** See [SUBMISSION.md](SUBMISSION.md)

## Important Notes

1. **API Key Security:** Never commit your `.env` file to Git
2. **Database:** SQLite is for development; use PostgreSQL for production
3. **Costs:** Gemini API has free tier; monitor your usage
4. **Rate Limits:** Be aware of Gemini API rate limits

## Common Commands Reference

```bash
# Start app
uvicorn app.main:app --reload

# Run tests
pytest

# Run tests with coverage
pytest --cov=app

# Build Docker image
docker build -t edtech-nlp2sql:latest .

# Run Docker container
docker run -p 8000:8000 -e GEMINI_API_KEY="key" edtech-nlp2sql:latest

# Apply Kubernetes resources
kubectl apply -f k8s-pod.yaml

# Check Kubernetes pods
kubectl get pods

# View logs
kubectl logs edtech-nlp2sql-pod
```

## Success Indicators

You'll know everything is working when:

1. ✅ Application starts without errors
2. ✅ http://localhost:8000/health returns `{"status": "healthy"}`
3. ✅ http://localhost:8000/docs shows interactive API documentation
4. ✅ POST /query returns valid SQL and results
5. ✅ GET /stats returns analytics data
6. ✅ All tests pass with `pytest`

---

**Ready to start? Run `setup.bat` (Windows) or `./setup.sh` (Linux/Mac)!**
