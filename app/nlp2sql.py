import openai
from app.config import get_settings
from typing import Optional

settings = get_settings()
openai.api_key = settings.openai_api_key


class NLP2SQLService:
    """Service for converting natural language to SQL queries using LLM"""
    
    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
        self.schema_info = """
Database Schema:
1. students table:
   - id (INTEGER, PRIMARY KEY)
   - name (VARCHAR)
   - grade (INTEGER)
   - created_at (DATETIME)

2. courses table:
   - id (INTEGER, PRIMARY KEY)
   - name (VARCHAR)
   - category (VARCHAR)

3. enrollments table:
   - id (INTEGER, PRIMARY KEY)
   - student_id (INTEGER, FOREIGN KEY -> students.id)
   - course_id (INTEGER, FOREIGN KEY -> courses.id)
   - enrolled_at (DATETIME)

Relationships:
- A student can have multiple enrollments
- A course can have multiple enrollments
- An enrollment belongs to one student and one course
"""
    
    def generate_sql(self, question: str) -> str:
        """
        Generate SQL query from natural language question using OpenAI GPT
        
        Args:
            question: Natural language question
            
        Returns:
            SQL query string
        """
        system_prompt = f"""You are an expert SQL query generator for an EdTech database.
{self.schema_info}

IMPORTANT RULES:
1. Generate ONLY SELECT queries
2. NEVER generate DELETE, DROP, UPDATE, INSERT, ALTER, or any data modification queries
3. Return ONLY the SQL query without any explanation or markdown formatting
4. Use proper SQL syntax for SQLite
5. Be precise with table and column names
6. Use JOINs when needed to answer questions involving multiple tables
7. Use WHERE clauses to filter data appropriately
8. Consider date/time filtering when questions mention specific years or time periods

Example:
Question: "How many students enrolled in Python courses in 2024?"
SQL: SELECT COUNT(DISTINCT e.student_id) FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.name LIKE '%Python%' AND strftime('%Y', e.enrolled_at) = '2024'
"""
        
        user_prompt = f"Generate a SQL query for this question: {question}"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                max_tokens=500
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            if sql_query.startswith("```"):
                sql_query = sql_query.split("\n", 1)[1]
                sql_query = sql_query.rsplit("```", 1)[0]
            
            sql_query = sql_query.strip()
            
            # Validate the query
            self._validate_query(sql_query)
            
            return sql_query
            
        except Exception as e:
            raise Exception(f"Failed to generate SQL: {str(e)}")
    
    def _validate_query(self, sql: str) -> None:
        """
        Validate that the SQL query is safe and only contains SELECT
        
        Args:
            sql: SQL query to validate
            
        Raises:
            ValueError: If query contains forbidden operations
        """
        sql_upper = sql.upper().strip()
        
        # Check if it starts with SELECT
        if not sql_upper.startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")
        
        # List of forbidden keywords
        forbidden_keywords = [
            "DELETE", "DROP", "UPDATE", "INSERT", "ALTER",
            "CREATE", "TRUNCATE", "REPLACE", "EXEC", "EXECUTE"
        ]
        
        # Check for forbidden keywords
        for keyword in forbidden_keywords:
            if keyword in sql_upper:
                raise ValueError(f"Query contains forbidden keyword: {keyword}")
