#!/usr/bin/env python3
import requests
import json

BASE_URL = "http://localhost:8000/api"

def test_create_connection():
    """Test creating a database connection"""
    data = {
        "name": "Test PostgreSQL",
        "host": "localhost",
        "port": 5432,
        "database_name": "testdb",
        "username": "testuser",
        "password": "testpass",
        "engine": "postgresql"
    }
    
    response = requests.post(f"{BASE_URL}/connections/create/", json=data)
    print(f"Create Connection: {response.status_code}")
    if response.status_code == 201:
        print(f"Connection ID: {response.json()['id']}")
        return response.json()['id']
    else:
        print(f"Error: {response.json()}")
        return None

def test_list_connections():
    """Test listing database connections"""
    response = requests.get(f"{BASE_URL}/connections/")
    print(f"List Connections: {response.status_code}")
    print(f"Connections: {len(response.json())}")
    return response.json()

def test_get_schema(connection_id):
    """Test getting database schema"""
    response = requests.get(f"{BASE_URL}/connections/{connection_id}/schema/")
    print(f"Get Schema: {response.status_code}")
    if response.status_code == 200:
        schema = response.json()
        print(f"Tables found: {list(schema['tables'].keys())}")
    else:
        print(f"Error: {response.json()}")

def test_natural_query(connection_id):
    """Test natural language query execution"""
    data = {
        "natural_query": "Show me all users",
        "database_connection_id": connection_id,
        "openai_api_key": "your-openai-api-key-here"
    }
    
    response = requests.post(f"{BASE_URL}/query/", json=data)
    print(f"Execute Query: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Generated SQL: {result['generated_sql']}")
        print(f"Results: {len(result.get('results', []))} rows")
    else:
        print(f"Error: {response.json()}")

def test_query_history():
    """Test getting query history"""
    response = requests.get(f"{BASE_URL}/history/")
    print(f"Query History: {response.status_code}")
    print(f"History entries: {len(response.json())}")

if __name__ == "__main__":
    print("Testing RDS NL Query API...")
    
    # Test connection creation
    connection_id = test_create_connection()
    
    if connection_id:
        # Test other endpoints
        test_list_connections()
        test_get_schema(connection_id)
        test_natural_query(connection_id)
        test_query_history()
    
    print("Testing completed!")