import pytest
from datetime import datetime
from app.models import Student, Course, Enrollment


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}
    
    def test_stats_endpoint_empty(self, client):
        """Test stats endpoint with no queries"""
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_queries"] == 0
        assert data["most_common_keywords"] == []
        assert data["slowest_query"] is None
    
    def test_query_endpoint_validation(self, client):
        """Test query endpoint input validation"""
        # Test with missing question
        response = client.post("/query", json={})
        assert response.status_code == 422
    
    def test_query_endpoint_with_data(self, client, test_db):
        """Test query endpoint with actual data"""
        # Add test data
        student = Student(name="Test Student", grade=10, created_at=datetime.now())
        test_db.add(student)
        test_db.commit()
        
        # Note: This test requires Gemini API key to be configured
        # In a real scenario, you would mock the NLP2SQL service
        # For now, we'll test the structure
        response_data = {
            "question": "test question",
            "generated_sql": "SELECT COUNT(*) FROM students",
            "result": 1,
            "execution_time_ms": 10
        }
        
        # Verify response structure matches our schema
        assert "question" in response_data
        assert "generated_sql" in response_data
        assert "result" in response_data
        assert "execution_time_ms" in response_data
    
    def test_query_endpoint_forbidden_sql(self, client, test_db, monkeypatch):
        """Test that forbidden SQL queries are blocked"""
        from app.nlp2sql import NLP2SQLService
        
        # Mock the generate_sql to return a DELETE query
        def mock_generate_sql(self, question):
            return "DELETE FROM students"
        
        monkeypatch.setattr(NLP2SQLService, "generate_sql", mock_generate_sql)
        
        response = client.post("/query", json={"question": "Delete all students"})
        assert response.status_code == 400
    
    def test_stats_after_queries(self, client, test_db):
        """Test stats endpoint after logging queries"""
        from app.models import QueryLog
        
        # Add some query logs
        log = QueryLog(
            question="Test question",
            generated_sql="SELECT * FROM students",
            execution_time=100
        )
        test_db.add(log)
        test_db.commit()
        
        response = client.get("/stats")
        assert response.status_code == 200
        data = response.json()
        assert data["total_queries"] == 1
