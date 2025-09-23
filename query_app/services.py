"""
Service layer for query processing.
Applies DRY principles and provides reusable business logic.
"""
import time
from typing import Dict, Any, Optional, Tuple
from .models import QueryHistory
from .database_inspector import DatabaseInspector
from .nl_to_sql import NLToSQLConverter
from .config import DatabaseConfig, APIConfig, ConfigValidator


class QueryService:
    """Service class for handling natural language queries."""
    
    def __init__(self):
        self._inspector = None
        self._converter = None
    
    def _get_inspector(self) -> DatabaseInspector:
        """Get database inspector instance (lazy loading)."""
        if self._inspector is None:
            db_config = DatabaseConfig.get_external_db_config()
            self._inspector = DatabaseInspector(db_config)
        return self._inspector
    
    def _get_converter(self) -> NLToSQLConverter:
        """Get NL to SQL converter instance (lazy loading)."""
        if self._converter is None:
            openai_key = APIConfig.get_openai_key()
            self._converter = NLToSQLConverter(openai_key)
        return self._converter
    
    def validate_configuration(self) -> Tuple[bool, Optional[str]]:
        """
        Validate system configuration.
        Returns (is_valid, error_message).
        """
        validation = ConfigValidator.validate_all()
        if not all(validation.values()):
            errors = ConfigValidator.get_validation_errors()
            return False, f"Configuration errors: {errors}"
        return True, None
    
    def get_database_schema(self) -> Dict[str, Any]:
        """Get database schema information."""
        inspector = self._get_inspector()
        return inspector.get_schema_info()
    
    def execute_natural_query(self, natural_query: str) -> Dict[str, Any]:
        """
        Execute a natural language query.
        Returns query results with metadata.
        """
        # Validate configuration
        is_valid, error = self.validate_configuration()
        if not is_valid:
            raise ValueError(error)
        
        # Get components
        inspector = self._get_inspector()
        converter = self._get_converter()
        
        # Get schema and convert query
        schema_info = inspector.get_schema_info()
        sql_query = converter.convert_to_sql(natural_query, schema_info)
        
        # Execute query
        start_time = time.time()
        query_result = inspector.execute_query(sql_query)
        execution_time = time.time() - start_time
        
        # Prepare response
        response_data = {
            'generated_sql': sql_query,
            'execution_time': execution_time,
            'columns': query_result.get('columns', []),
            'results': query_result.get('results', [])
        }
        
        return response_data
    
    def save_query_to_history(self, natural_query: str, sql_query: str, 
                            execution_time: float, success: bool, 
                            error_message: str = '') -> QueryHistory:
        """Save query execution to history."""
        return QueryHistory.objects.create(
            natural_query=natural_query,
            generated_sql=sql_query,
            execution_time=execution_time,
            success=success,
            error_message=error_message
        )
    
    def get_query_history(self, limit: int = 50) -> list:
        """Get query history with pagination."""
        return list(QueryHistory.objects.all().order_by('-created_at')[:limit])


class ErrorHandler:
    """Centralized error handling using CBT principles."""
    
    @staticmethod
    def handle_query_error(error: Exception, natural_query: str, 
                          sql_query: str = '') -> Dict[str, str]:
        """
        Handle query execution errors consistently.
        Returns standardized error response.
        """
        error_types = {
            'ValueError': 'Configuration Error',
            'ConnectionError': 'Database Connection Error',
            'TimeoutError': 'Query Timeout Error',
            'Exception': 'Query Execution Error'
        }
        
        error_type = error_types.get(type(error).__name__, 'Unknown Error')
        
        return {
            'error_type': error_type,
            'error_message': str(error),
            'suggestion': ErrorHandler._get_error_suggestion(error)
        }
    
    @staticmethod
    def _get_error_suggestion(error: Exception) -> str:
        """Get user-friendly error suggestions."""
        error_message = str(error).lower()
        
        if 'connection' in error_message:
            return "Please check your database configuration in the .env file."
        elif 'timeout' in error_message:
            return "The query took too long to execute. Try simplifying your query."
        elif 'syntax' in error_message:
            return "There was an issue with the generated SQL. Try rephrasing your query."
        else:
            return "Please check your query and try again."


class ResponseBuilder:
    """Build consistent API responses using DRY principles."""
    
    @staticmethod
    def success_response(data: Dict[str, Any], message: str = "Success") -> Dict[str, Any]:
        """Build success response."""
        return {
            'status': 'success',
            'message': message,
            'data': data
        }
    
    @staticmethod
    def error_response(error: str, error_type: str = "Error") -> Dict[str, Any]:
        """Build error response."""
        return {
            'status': 'error',
            'error_type': error_type,
            'error': error
        }
    
    @staticmethod
    def query_response(query_data: Dict[str, Any]) -> Dict[str, Any]:
        """Build query execution response."""
        return {
            'generated_sql': query_data['generated_sql'],
            'execution_time': query_data['execution_time'],
            'columns': query_data.get('columns', []),
            'results': query_data.get('results', [])
        }
