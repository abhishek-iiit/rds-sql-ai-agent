import openai
import json
from typing import Dict, Any

class NLToSQLConverter:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    def convert_to_sql(self, natural_query: str, schema_info: Dict[str, Any]) -> str:
        schema_description = self._format_schema_for_prompt(schema_info)
        
        prompt = f"""
You are a SQL expert. Convert the following natural language query to SQL based on the provided database schema.

Database Schema:
{schema_description}

Natural Language Query: {natural_query}

Rules:
1. Generate only valid SQL for {schema_info['engine']}
2. Use proper table and column names from the schema
3. Include appropriate JOINs when querying multiple tables
4. Use LIMIT for potentially large result sets
5. Return only the SQL query, no explanations

SQL Query:"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a SQL expert that converts natural language to SQL queries."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        sql_query = response.choices[0].message.content.strip()
        
        # Clean up the response
        if sql_query.startswith('```sql'):
            sql_query = sql_query[6:]
        if sql_query.endswith('```'):
            sql_query = sql_query[:-3]
        
        return sql_query.strip()
    
    def _format_schema_for_prompt(self, schema_info: Dict[str, Any]) -> str:
        schema_text = f"Database Engine: {schema_info['engine']}\n\nTables:\n"
        
        for table_name, table_info in schema_info['tables'].items():
            schema_text += f"\n{table_name}:\n"
            
            # Add columns
            for column in table_info['columns']:
                nullable = "NULL" if column['nullable'] else "NOT NULL"
                schema_text += f"  - {column['name']} ({column['type']}) {nullable}\n"
            
            # Add relationships
            if table_info['relationships']:
                schema_text += "  Foreign Keys:\n"
                for rel in table_info['relationships']:
                    schema_text += f"    - {rel['column']} -> {rel['references_table']}.{rel['references_column']}\n"
        
        return schema_text