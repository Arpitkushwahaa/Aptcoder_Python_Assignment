import pytest
from datetime import datetime
from app.models import Student, Course, Enrollment
from app.sql_executor import SQLExecutor


class TestSQLExecutor:
    """Test cases for SQL execution"""
    
    def test_execute_simple_query(self, test_db):
        """Test executing a simple SELECT query"""
        # Add test data
        student = Student(name="Test Student", grade=10, created_at=datetime.now())
        test_db.add(student)
        test_db.commit()
        
        executor = SQLExecutor()
        sql = "SELECT COUNT(*) as count FROM students"
        result, execution_time = executor.execute_query(test_db, sql, "How many students?")
        
        assert result == 1
        assert execution_time >= 0
    
    def test_execute_query_with_results(self, test_db):
        """Test executing query that returns multiple rows"""
        # Add test data
        students = [
            Student(name="Alice", grade=10, created_at=datetime.now()),
            Student(name="Bob", grade=11, created_at=datetime.now())
        ]
        test_db.add_all(students)
        test_db.commit()
        
        executor = SQLExecutor()
        sql = "SELECT name, grade FROM students ORDER BY name"
        result, execution_time = executor.execute_query(test_db, sql, "List students")
        
        assert len(result) == 2
        assert result[0]["name"] == "Alice"
        assert result[1]["name"] == "Bob"
        assert execution_time >= 0
    
    def test_execute_query_no_results(self, test_db):
        """Test executing query with no results"""
        executor = SQLExecutor()
        sql = "SELECT * FROM students WHERE grade > 100"
        result, execution_time = executor.execute_query(test_db, sql, "No students")
        
        assert result == []
        assert execution_time >= 0
    
    def test_execute_invalid_query(self, test_db):
        """Test executing invalid SQL raises exception"""
        executor = SQLExecutor()
        sql = "SELECT * FROM nonexistent_table"
        
        with pytest.raises(Exception):
            executor.execute_query(test_db, sql, "Invalid query")
    
    def test_process_scalar_result(self):
        """Test processing scalar results"""
        executor = SQLExecutor()
        
        # Mock row with single value
        class MockRow:
            def __init__(self, value):
                self._mapping = {"count": value}
                self._data = (value,)
            
            def __getitem__(self, index):
                return self._data[index]
            
            def __len__(self):
                return len(self._data)
        
        rows = [MockRow(42)]
        result = executor._process_results(rows)
        assert result == 42
