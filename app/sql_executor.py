from sqlalchemy.orm import Session
from sqlalchemy import text
from app.models import QueryLog
from typing import Any, List, Union
import time


class SQLExecutor:
    """Service for executing SQL queries safely"""
    
    def execute_query(self, db: Session, sql: str, question: str) -> tuple[Any, int]:
        """
        Execute SQL query and log the execution
        
        Args:
            db: Database session
            sql: SQL query to execute
            question: Original question
            
        Returns:
            Tuple of (result, execution_time_ms)
        """
        start_time = time.time()
        
        try:
            # Execute the query
            result = db.execute(text(sql))
            
            # Fetch results
            rows = result.fetchall()
            
            # Calculate execution time
            execution_time_ms = int((time.time() - start_time) * 1000)
            
            # Process results
            processed_result = self._process_results(rows)
            
            # Log the query
            self._log_query(db, question, sql, execution_time_ms)
            
            return processed_result, execution_time_ms
            
        except Exception as e:
            execution_time_ms = int((time.time() - start_time) * 1000)
            raise Exception(f"Query execution failed: {str(e)}")
    
    def _process_results(self, rows: List) -> Union[int, float, str, List[dict]]:
        """
        Process query results into appropriate format
        
        Args:
            rows: Raw query results
            
        Returns:
            Processed results (scalar or list of dicts)
        """
        if not rows:
            return []
        
        # If single row with single column (scalar result)
        if len(rows) == 1 and len(rows[0]) == 1:
            value = rows[0][0]
            return value if value is not None else 0
        
        # Convert rows to list of dictionaries
        result = []
        for row in rows:
            row_dict = dict(row._mapping)
            result.append(row_dict)
        
        return result
    
    def _log_query(self, db: Session, question: str, sql: str, execution_time_ms: int) -> None:
        """
        Log query execution for analytics
        
        Args:
            db: Database session
            question: Original question
            sql: Generated SQL
            execution_time_ms: Execution time in milliseconds
        """
        try:
            query_log = QueryLog(
                question=question,
                generated_sql=sql,
                execution_time=execution_time_ms
            )
            db.add(query_log)
            db.commit()
        except Exception as e:
            print(f"Failed to log query: {e}")
            db.rollback()
