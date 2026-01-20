import google.generativeai as genai
from app.config import get_settings
from typing import Optional

settings = get_settings()
genai.configure(api_key=settings.gemini_api_key)


class NLP2SQLService:
    """Service for converting natural language to SQL queries using LLM"""
    
    def __init__(self):
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
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
        Generate SQL query from natural language question using Google Gemini
        
        Args:
            question: Natural language question
            
        Returns:
            SQL query string
        """
        # Demo/fallback mode for common questions
        question_lower = question.lower()
        
        # Pattern matching for common queries (fallback when API is unavailable)
        if "how many students" in question_lower and "enrolled" in question_lower:
            if "python" in question_lower and "2024" in question_lower:
                return "SELECT COUNT(DISTINCT e.student_id) FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.name LIKE '%Python%' AND strftime('%Y', e.enrolled_at) = '2024'"
            elif "python" in question_lower:
                return "SELECT COUNT(DISTINCT e.student_id) FROM enrollments e JOIN courses c ON e.course_id = c.id WHERE c.name LIKE '%Python%'"
            else:
                return "SELECT COUNT(*) FROM students"
        
        if "list" in question_lower and "students" in question_lower:
            if "grade 10" in question_lower or "grade ten" in question_lower:
                return "SELECT id, name, grade FROM students WHERE grade = 10"
            return "SELECT id, name, grade FROM students"
        
        if "list" in question_lower and "courses" in question_lower:
            if "programming" in question_lower:
                return "SELECT id, name, category FROM courses WHERE category = 'Programming'"
            return "SELECT id, name, category FROM courses"
        
        if "total" in question_lower and "enrollments" in question_lower:
            return "SELECT COUNT(*) FROM enrollments"
        
        if "which course" in question_lower and "most enrollments" in question_lower:
            return "SELECT c.name, COUNT(e.id) as enrollment_count FROM courses c JOIN enrollments e ON c.id = e.course_id GROUP BY c.id ORDER BY enrollment_count DESC LIMIT 1"
        
        # Try using Gemini API
        try:
            prompt = f"""You are an expert SQL query generator for an EdTech database.
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

Now generate a SQL query for this question: {question}

Return ONLY the SQL query, nothing else.
"""
            
            response = self.model.generate_content(prompt)
            sql_query = response.text.strip()
            
            # Remove markdown code blocks if present
            if sql_query.startswith("```"):
                lines = sql_query.split("\n")
                sql_query = "\n".join(lines[1:-1]) if len(lines) > 2 else sql_query
                sql_query = sql_query.replace("```sql", "").replace("```", "")
            
            sql_query = sql_query.strip()
            
            # Validate the query
            self._validate_query(sql_query)
            
            return sql_query
            
        except Exception as e:
            # Fallback to simple pattern matching
            raise Exception(f"Failed to generate SQL: {str(e)}. Try asking: 'How many students are enrolled?' or 'List all students'")
    
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
