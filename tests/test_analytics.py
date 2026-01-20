import pytest
from datetime import datetime
from app.models import Student, Course, Enrollment, QueryLog
from app.analytics import AnalyticsService


class TestAnalytics:
    """Test cases for analytics service"""
    
    def test_get_stats_no_queries(self, test_db):
        """Test stats with no queries"""
        service = AnalyticsService()
        stats = service.get_stats(test_db)
        
        assert stats["total_queries"] == 0
        assert stats["most_common_keywords"] == []
        assert stats["slowest_query"] is None
    
    def test_get_stats_with_queries(self, test_db):
        """Test stats with query logs"""
        # Add query logs
        logs = [
            QueryLog(
                question="How many students enrolled?",
                generated_sql="SELECT COUNT(*) FROM students",
                execution_time=100
            ),
            QueryLog(
                question="List all courses",
                generated_sql="SELECT * FROM courses",
                execution_time=50
            ),
            QueryLog(
                question="How many Python students?",
                generated_sql="SELECT COUNT(*) FROM enrollments",
                execution_time=200
            )
        ]
        test_db.add_all(logs)
        test_db.commit()
        
        service = AnalyticsService()
        stats = service.get_stats(test_db)
        
        assert stats["total_queries"] == 3
        assert len(stats["most_common_keywords"]) > 0
        assert stats["slowest_query"] is not None
        assert stats["slowest_query"]["execution_time_ms"] == 200
    
    def test_extract_keywords(self):
        """Test keyword extraction"""
        service = AnalyticsService()
        questions = [
            "How many students enrolled?",
            "List all students",
            "How many courses available?"
        ]
        
        keywords = service._extract_keywords(questions)
        
        # Should contain "students" and "enrolled"
        keyword_words = [k["keyword"] for k in keywords]
        assert "students" in keyword_words
    
    def test_extract_keywords_filters_stopwords(self):
        """Test that stopwords are filtered out"""
        service = AnalyticsService()
        questions = ["How many students are there?"]
        
        keywords = service._extract_keywords(questions)
        keyword_words = [k["keyword"] for k in keywords]
        
        # Stopwords should be filtered
        assert "how" not in keyword_words
        assert "many" not in keyword_words
        assert "are" not in keyword_words
        assert "there" not in keyword_words
    
    def test_slowest_query_tracking(self, test_db):
        """Test that slowest query is correctly identified"""
        logs = [
            QueryLog(
                question="Fast query",
                generated_sql="SELECT 1",
                execution_time=10
            ),
            QueryLog(
                question="Slow query",
                generated_sql="SELECT * FROM enrollments",
                execution_time=500
            ),
            QueryLog(
                question="Medium query",
                generated_sql="SELECT * FROM students",
                execution_time=100
            )
        ]
        test_db.add_all(logs)
        test_db.commit()
        
        service = AnalyticsService()
        stats = service.get_stats(test_db)
        
        assert stats["slowest_query"]["question"] == "Slow query"
        assert stats["slowest_query"]["execution_time_ms"] == 500
