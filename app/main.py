from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import QueryRequest, QueryResponse, StatsResponse
from app.nlp2sql import NLP2SQLService
from app.sql_executor import SQLExecutor
from app.analytics import AnalyticsService

# Initialize FastAPI app
app = FastAPI(
    title="EdTech NLP-to-SQL API",
    description="AI-powered backend service that converts natural language questions into SQL queries",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
nlp2sql_service = NLP2SQLService()
sql_executor = SQLExecutor()
analytics_service = AnalyticsService()


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "EdTech NLP-to-SQL API",
        "version": "1.0.0",
        "endpoints": {
            "query": "POST /query",
            "stats": "GET /stats"
        }
    }


@app.post("/query", response_model=QueryResponse)
async def query_endpoint(
    request: QueryRequest,
    db: Session = Depends(get_db)
):
    """
    Convert natural language question to SQL and execute it
    
    Args:
        request: Query request containing the natural language question
        db: Database session
        
    Returns:
        QueryResponse with SQL, results, and execution time
    """
    try:
        # Generate SQL from natural language
        sql_query = nlp2sql_service.generate_sql(request.question)
        
        # Execute the SQL query
        result, execution_time_ms = sql_executor.execute_query(
            db, sql_query, request.question
        )
        
        return QueryResponse(
            question=request.question,
            generated_sql=sql_query,
            result=result,
            execution_time_ms=execution_time_ms
        )
        
    except ValueError as e:
        print(f"Validation Error: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"Server Error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


@app.get("/stats", response_model=StatsResponse)
async def stats_endpoint(db: Session = Depends(get_db)):
    """
    Get analytics statistics about queries
    
    Args:
        db: Database session
        
    Returns:
        StatsResponse with analytics data
    """
    try:
        stats = analytics_service.get_stats(db)
        return StatsResponse(**stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
