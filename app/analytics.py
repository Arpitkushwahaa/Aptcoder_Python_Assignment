from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import QueryLog
from typing import List, Dict, Any, Optional
import re
from collections import Counter


class AnalyticsService:
    """Service for query analytics"""
    
    def get_stats(self, db: Session) -> Dict[str, Any]:
        """
        Get analytics statistics
        
        Args:
            db: Database session
            
        Returns:
            Dictionary containing analytics stats
        """
        # Total number of queries
        total_queries = db.query(QueryLog).count()
        
        # Get all questions for keyword analysis
        queries = db.query(QueryLog.question).all()
        keywords = self._extract_keywords([q[0] for q in queries])
        
        # Get slowest query
        slowest_query = db.query(QueryLog).order_by(desc(QueryLog.execution_time)).first()
        
        slowest_query_data = None
        if slowest_query:
            slowest_query_data = {
                "question": slowest_query.question,
                "generated_sql": slowest_query.generated_sql,
                "execution_time_ms": slowest_query.execution_time,
                "created_at": slowest_query.created_at.isoformat()
            }
        
        return {
            "total_queries": total_queries,
            "most_common_keywords": keywords,
            "slowest_query": slowest_query_data
        }
    
    def _extract_keywords(self, questions: List[str]) -> List[Dict[str, Any]]:
        """
        Extract and count common keywords from questions
        
        Args:
            questions: List of question strings
            
        Returns:
            List of dictionaries with keyword and count
        """
        # Common stop words to exclude
        stop_words = {
            'a', 'an', 'and', 'are', 'as', 'at', 'be', 'by', 'for', 'from',
            'has', 'he', 'in', 'is', 'it', 'its', 'of', 'on', 'that', 'the',
            'to', 'was', 'were', 'will', 'with', 'how', 'many', 'what', 'when',
            'where', 'who', 'which', 'did', 'do', 'does'
        }
        
        all_words = []
        for question in questions:
            # Convert to lowercase and extract words
            words = re.findall(r'\b[a-z]+\b', question.lower())
            # Filter out stop words and short words
            filtered_words = [w for w in words if w not in stop_words and len(w) > 2]
            all_words.extend(filtered_words)
        
        # Count keywords
        keyword_counts = Counter(all_words)
        
        # Get top 10 most common keywords
        most_common = keyword_counts.most_common(10)
        
        return [{"keyword": word, "count": count} for word, count in most_common]
