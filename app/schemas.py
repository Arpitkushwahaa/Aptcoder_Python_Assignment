from pydantic import BaseModel
from typing import Any, List, Dict, Optional


class QueryRequest(BaseModel):
    """Request model for natural language query"""
    question: str


class QueryResponse(BaseModel):
    """Response model for query execution"""
    question: str
    generated_sql: str
    result: Any
    execution_time_ms: int


class StatsResponse(BaseModel):
    """Response model for analytics stats"""
    total_queries: int
    most_common_keywords: List[Dict[str, Any]]
    slowest_query: Optional[Dict[str, Any]]
