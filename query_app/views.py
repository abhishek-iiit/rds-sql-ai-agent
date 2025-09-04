import time
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import DatabaseConnection, QueryHistory
from .serializers import (
    DatabaseConnectionSerializer, DatabaseConnectionCreateSerializer,
    QueryRequestSerializer, QueryResponseSerializer, QueryHistorySerializer
)
from .database_inspector import DatabaseInspector
from .nl_to_sql import NLToSQLConverter

@api_view(['POST'])
def create_database_connection(request):
    serializer = DatabaseConnectionCreateSerializer(data=request.data)
    if serializer.is_valid():
        # Test connection before saving
        try:
            inspector = DatabaseInspector({
                'host': serializer.validated_data['host'],
                'port': serializer.validated_data['port'],
                'database_name': serializer.validated_data['database_name'],
                'username': serializer.validated_data['username'],
                'password': serializer.validated_data['password'],
                'engine': serializer.validated_data['engine']
            })
            inspector.get_connection().close()
        except Exception as e:
            return Response({'error': f'Connection failed: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create user if not exists (simplified for demo)
        user, _ = User.objects.get_or_create(username='demo_user')
        
        connection = serializer.save(user=user)
        return Response(DatabaseConnectionSerializer(connection).data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def list_database_connections(request):
    user, _ = User.objects.get_or_create(username='demo_user')
    connections = DatabaseConnection.objects.filter(user=user)
    serializer = DatabaseConnectionSerializer(connections, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_database_schema(request, connection_id):
    try:
        user, _ = User.objects.get_or_create(username='demo_user')
        connection = DatabaseConnection.objects.get(id=connection_id, user=user)
        
        inspector = DatabaseInspector({
            'host': connection.host,
            'port': connection.port,
            'database_name': connection.database_name,
            'username': connection.username,
            'password': connection.password,
            'engine': connection.engine
        })
        
        schema_info = inspector.get_schema_info()
        return Response(schema_info)
    
    except DatabaseConnection.DoesNotExist:
        return Response({'error': 'Database connection not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def execute_natural_query(request):
    serializer = QueryRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user, _ = User.objects.get_or_create(username='demo_user')
        connection = DatabaseConnection.objects.get(
            id=serializer.validated_data['database_connection_id'], 
            user=user
        )
        
        # Get database schema
        inspector = DatabaseInspector({
            'host': connection.host,
            'port': connection.port,
            'database_name': connection.database_name,
            'username': connection.username,
            'password': connection.password,
            'engine': connection.engine
        })
        
        schema_info = inspector.get_schema_info()
        
        # Convert natural language to SQL
        converter = NLToSQLConverter(serializer.validated_data['openai_api_key'])
        sql_query = converter.convert_to_sql(
            serializer.validated_data['natural_query'], 
            schema_info
        )
        
        # Execute SQL query
        start_time = time.time()
        query_result = inspector.execute_query(sql_query)
        execution_time = time.time() - start_time
        
        # Save to history
        QueryHistory.objects.create(
            user=user,
            database_connection=connection,
            natural_query=serializer.validated_data['natural_query'],
            generated_sql=sql_query,
            execution_time=execution_time,
            success=True
        )
        
        response_data = {
            'generated_sql': sql_query,
            'execution_time': execution_time,
            'columns': query_result.get('columns', []),
            'results': query_result.get('results', [])
        }
        
        return Response(QueryResponseSerializer(response_data).data)
    
    except DatabaseConnection.DoesNotExist:
        return Response({'error': 'Database connection not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        # Save failed query to history
        try:
            QueryHistory.objects.create(
                user=user,
                database_connection=connection,
                natural_query=serializer.validated_data['natural_query'],
                generated_sql=sql_query if 'sql_query' in locals() else '',
                success=False,
                error_message=str(e)
            )
        except:
            pass
        
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def get_query_history(request):
    user, _ = User.objects.get_or_create(username='demo_user')
    history = QueryHistory.objects.filter(user=user).order_by('-created_at')[:50]
    serializer = QueryHistorySerializer(history, many=True)
    return Response(serializer.data)