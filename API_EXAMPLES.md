# Example API Requests

This document contains example `curl` commands and Python requests for testing the API.

## Health Check

### cURL
```bash
curl http://localhost:8000/health
```

### Python
```python
import requests
response = requests.get("http://localhost:8000/health")
print(response.json())
```

## Query Endpoint

### Example 1: Count Students

#### cURL
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many students are enrolled?"}'
```

#### Python
```python
import requests
response = requests.post(
    "http://localhost:8000/query",
    json={"question": "How many students are enrolled?"}
)
print(response.json())
```

### Example 2: Python Courses in 2024

#### cURL
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many students enrolled in Python courses in 2024?"}'
```

#### Python
```python
import requests
response = requests.post(
    "http://localhost:8000/query",
    json={"question": "How many students enrolled in Python courses in 2024?"}
)
result = response.json()
print(f"SQL: {result['generated_sql']}")
print(f"Result: {result['result']}")
print(f"Time: {result['execution_time_ms']} ms")
```

### Example 3: List Students

#### cURL
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "List all students in grade 10"}'
```

#### Python
```python
import requests
response = requests.post(
    "http://localhost:8000/query",
    json={"question": "List all students in grade 10"}
)
print(response.json())
```

### Example 4: Course Enrollments

#### cURL
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Which course has the most enrollments?"}'
```

#### Python
```python
import requests
response = requests.post(
    "http://localhost:8000/query",
    json={"question": "Which course has the most enrollments?"}
)
print(response.json())
```

### Example 5: Programming Courses

#### cURL
```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all courses in the Programming category"}'
```

## Stats Endpoint

### cURL
```bash
curl http://localhost:8000/stats
```

### Python
```python
import requests
response = requests.get("http://localhost:8000/stats")
stats = response.json()
print(f"Total queries: {stats['total_queries']}")
print(f"Common keywords: {stats['most_common_keywords']}")
print(f"Slowest query: {stats['slowest_query']}")
```

## PowerShell Examples (Windows)

### Query Endpoint
```powershell
$body = @{
    question = "How many students enrolled in Python courses in 2024?"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/query" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body
```

### Stats Endpoint
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/stats" -Method Get
```

### Health Check
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

## Expected Responses

### Query Response
```json
{
  "question": "How many students enrolled in Python courses in 2024?",
  "generated_sql": "SELECT COUNT(DISTINCT e.student_id) FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.name LIKE '%Python%' AND strftime('%Y', e.enrolled_at) = '2024'",
  "result": 5,
  "execution_time_ms": 45
}
```

### Stats Response
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

## Error Responses

### Invalid Query (Forbidden SQL)
```json
{
  "detail": "Query contains forbidden keyword: DELETE"
}
```

### Missing Question
```json
{
  "detail": [
    {
      "loc": ["body", "question"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### API Error
```json
{
  "detail": "Failed to generate SQL: <error message>"
}
```
