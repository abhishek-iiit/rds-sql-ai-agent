# RDS Natural Language Query System

A production-ready Django REST API that converts natural language queries to SQL and executes them against AWS RDS databases.

## Features

- **Natural Language to SQL**: Uses OpenAI GPT-4 to convert plain English to SQL
- **Database Schema Discovery**: Automatically inspects database structure and relationships
- **Multi-Database Support**: PostgreSQL and MySQL support
- **Query History**: Tracks all queries and their performance
- **Production Ready**: Proper error handling, validation, and security

## Setup

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your credentials
```

3. **Database Migration**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

4. **Run Server**
```bash
python manage.py runserver
```

## API Endpoints

### 1. Create Database Connection
```bash
POST /api/connections/create/
{
    "name": "My RDS Database",
    "host": "your-rds-endpoint.amazonaws.com",
    "port": 5432,
    "database_name": "mydb",
    "username": "dbuser",
    "password": "dbpass",
    "engine": "postgresql"
}
```

### 2. List Connections
```bash
GET /api/connections/
```

### 3. Get Database Schema
```bash
GET /api/connections/{id}/schema/
```

### 4. Execute Natural Language Query
```bash
POST /api/query/
{
    "natural_query": "Show me all users who registered last month",
    "database_connection_id": 1,
    "openai_api_key": "sk-..."
}
```

### 5. Query History
```bash
GET /api/history/
```

## Usage Examples

### Natural Language Queries:
- "Show me all customers from New York"
- "What are the top 10 products by sales?"
- "Find users who haven't logged in for 30 days"
- "Get the average order value by month"

## Security Features

- Input validation and sanitization
- SQL injection prevention
- Credential encryption (implement in production)
- Query execution limits
- Error handling without data exposure

## Production Deployment

1. **Environment Variables**
   - Set `DEBUG=False`
   - Use strong `SECRET_KEY`
   - Configure proper database settings

2. **Security Enhancements**
   - Implement credential encryption
   - Add authentication/authorization
   - Set up HTTPS
   - Configure CORS properly

3. **Performance**
   - Add query caching
   - Implement connection pooling
   - Set up monitoring

## Architecture

```
User Input (Natural Language)
    ↓
OpenAI GPT-4 (NL to SQL Conversion)
    ↓
Database Inspector (Schema Analysis)
    ↓
SQL Execution (AWS RDS)
    ↓
Results Formatting
    ↓
Response to User
```

## Error Handling

The system handles:
- Invalid database connections
- Malformed SQL queries
- OpenAI API failures
- Database execution errors
- Network timeouts