"""
Example script demonstrating how to use the EdTech NLP-to-SQL API
"""
import requests
import json
from typing import Dict, Any


class EdTechAPIClient:
    """Client for interacting with the EdTech NLP-to-SQL API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def query(self, question: str) -> Dict[str, Any]:
        """
        Send a natural language query to the API
        
        Args:
            question: Natural language question
            
        Returns:
            Response containing SQL, result, and execution time
        """
        response = requests.post(
            f"{self.base_url}/query",
            json={"question": question}
        )
        response.raise_for_status()
        return response.json()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get analytics statistics"""
        response = requests.get(f"{self.base_url}/stats")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, str]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()


def main():
    """Main function demonstrating API usage"""
    
    # Initialize client
    client = EdTechAPIClient()
    
    # Check health
    print("=" * 60)
    print("Health Check")
    print("=" * 60)
    health = client.health_check()
    print(f"Status: {health['status']}")
    print()
    
    # Example queries
    questions = [
        "How many students are enrolled?",
        "How many students enrolled in Python courses in 2024?",
        "List all courses in the Programming category",
        "What is the total number of enrollments?",
        "Show me students in grade 10",
    ]
    
    print("=" * 60)
    print("Example Queries")
    print("=" * 60)
    
    for i, question in enumerate(questions, 1):
        print(f"\n[Query {i}] {question}")
        print("-" * 60)
        
        try:
            result = client.query(question)
            
            print(f"Generated SQL:")
            print(f"  {result['generated_sql']}")
            print(f"\nResult:")
            print(f"  {json.dumps(result['result'], indent=2)}")
            print(f"\nExecution Time: {result['execution_time_ms']} ms")
            
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")
    
    # Get statistics
    print("\n" + "=" * 60)
    print("Analytics Statistics")
    print("=" * 60)
    
    try:
        stats = client.get_stats()
        
        print(f"\nTotal Queries: {stats['total_queries']}")
        
        print("\nMost Common Keywords:")
        for keyword in stats['most_common_keywords'][:5]:
            print(f"  - {keyword['keyword']}: {keyword['count']} times")
        
        if stats['slowest_query']:
            print("\nSlowest Query:")
            print(f"  Question: {stats['slowest_query']['question']}")
            print(f"  SQL: {stats['slowest_query']['generated_sql']}")
            print(f"  Execution Time: {stats['slowest_query']['execution_time_ms']} ms")
        
    except requests.exceptions.RequestException as e:
        print(f"Error getting stats: {e}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    except Exception as e:
        print(f"\nFatal error: {e}")
