import pytest
from app.nlp2sql import NLP2SQLService


class TestNLP2SQL:
    """Test cases for NLP to SQL conversion"""
    
    def test_validate_select_query(self):
        """Test that SELECT queries are accepted"""
        service = NLP2SQLService()
        sql = "SELECT * FROM students"
        # Should not raise an exception
        service._validate_query(sql)
    
    def test_validate_delete_query_blocked(self):
        """Test that DELETE queries are blocked"""
        service = NLP2SQLService()
        sql = "DELETE FROM students WHERE id = 1"
        with pytest.raises(ValueError, match="forbidden keyword"):
            service._validate_query(sql)
    
    def test_validate_drop_query_blocked(self):
        """Test that DROP queries are blocked"""
        service = NLP2SQLService()
        sql = "DROP TABLE students"
        with pytest.raises(ValueError, match="forbidden keyword"):
            service._validate_query(sql)
    
    def test_validate_update_query_blocked(self):
        """Test that UPDATE queries are blocked"""
        service = NLP2SQLService()
        sql = "UPDATE students SET name = 'Test' WHERE id = 1"
        with pytest.raises(ValueError, match="forbidden keyword"):
            service._validate_query(sql)
    
    def test_validate_insert_query_blocked(self):
        """Test that INSERT queries are blocked"""
        service = NLP2SQLService()
        sql = "INSERT INTO students (name, grade) VALUES ('Test', 10)"
        with pytest.raises(ValueError, match="forbidden keyword"):
            service._validate_query(sql)
    
    def test_validate_non_select_start_blocked(self):
        """Test that queries not starting with SELECT are blocked"""
        service = NLP2SQLService()
        sql = "EXPLAIN SELECT * FROM students"
        with pytest.raises(ValueError, match="Only SELECT queries are allowed"):
            service._validate_query(sql)
    
    def test_schema_info_contains_tables(self):
        """Test that schema info contains all required tables"""
        service = NLP2SQLService()
        assert "students" in service.schema_info
        assert "courses" in service.schema_info
        assert "enrollments" in service.schema_info
    
    def test_schema_info_contains_columns(self):
        """Test that schema info contains important columns"""
        service = NLP2SQLService()
        assert "student_id" in service.schema_info
        assert "course_id" in service.schema_info
        assert "enrolled_at" in service.schema_info
