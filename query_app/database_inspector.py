import psycopg2
import pymysql
from typing import Dict, List, Any

class DatabaseInspector:
    def __init__(self, connection_params: Dict[str, Any]):
        self.connection_params = connection_params
        self.engine = connection_params['engine']
    
    def get_connection(self):
        if self.engine == 'postgresql':
            return psycopg2.connect(
                host=self.connection_params['host'],
                port=self.connection_params['port'],
                database=self.connection_params['database_name'],
                user=self.connection_params['username'],
                password=self.connection_params['password']
            )
        elif self.engine == 'mysql':
            return pymysql.connect(
                host=self.connection_params['host'],
                port=self.connection_params['port'],
                database=self.connection_params['database_name'],
                user=self.connection_params['username'],
                password=self.connection_params['password']
            )
    
    def get_schema_info(self) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.engine == 'postgresql':
                return self._get_postgresql_schema(cursor)
            elif self.engine == 'mysql':
                return self._get_mysql_schema(cursor)
        finally:
            cursor.close()
            conn.close()
    
    def _get_postgresql_schema(self, cursor) -> Dict[str, Any]:
        # Get tables and columns
        cursor.execute("""
            SELECT t.table_name, c.column_name, c.data_type, c.is_nullable
            FROM information_schema.tables t
            JOIN information_schema.columns c ON t.table_name = c.table_name
            WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position
        """)
        
        tables = {}
        for row in cursor.fetchall():
            table_name, column_name, data_type, is_nullable = row
            if table_name not in tables:
                tables[table_name] = {'columns': [], 'relationships': []}
            tables[table_name]['columns'].append({
                'name': column_name,
                'type': data_type,
                'nullable': is_nullable == 'YES'
            })
        
        # Get foreign key relationships
        cursor.execute("""
            SELECT tc.table_name, kcu.column_name, ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = 'public'
        """)
        
        for row in cursor.fetchall():
            table_name, column_name, foreign_table, foreign_column = row
            if table_name in tables:
                tables[table_name]['relationships'].append({
                    'column': column_name,
                    'references_table': foreign_table,
                    'references_column': foreign_column
                })
        
        return {'tables': tables, 'engine': 'postgresql'}
    
    def _get_mysql_schema(self, cursor) -> Dict[str, Any]:
        # Get tables and columns
        cursor.execute("""
            SELECT t.table_name, c.column_name, c.data_type, c.is_nullable
            FROM information_schema.tables t
            JOIN information_schema.columns c ON t.table_name = c.table_name
            WHERE t.table_schema = DATABASE() AND t.table_type = 'BASE TABLE'
            ORDER BY t.table_name, c.ordinal_position
        """)
        
        tables = {}
        for row in cursor.fetchall():
            table_name, column_name, data_type, is_nullable = row
            if table_name not in tables:
                tables[table_name] = {'columns': [], 'relationships': []}
            tables[table_name]['columns'].append({
                'name': column_name,
                'type': data_type,
                'nullable': is_nullable == 'YES'
            })
        
        # Get foreign key relationships
        cursor.execute("""
            SELECT table_name, column_name, referenced_table_name, referenced_column_name
            FROM information_schema.key_column_usage
            WHERE table_schema = DATABASE() AND referenced_table_name IS NOT NULL
        """)
        
        for row in cursor.fetchall():
            table_name, column_name, foreign_table, foreign_column = row
            if table_name in tables:
                tables[table_name]['relationships'].append({
                    'column': column_name,
                    'references_table': foreign_table,
                    'references_column': foreign_column
                })
        
        return {'tables': tables, 'engine': 'mysql'}
    
    def execute_query(self, sql: str) -> Dict[str, Any]:
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute(sql)
            
            if cursor.description:
                columns = [desc[0] for desc in cursor.description]
                results = cursor.fetchall()
                return {
                    'columns': columns,
                    'results': [dict(zip(columns, row)) for row in results],
                    'row_count': len(results)
                }
            else:
                return {'message': 'Query executed successfully', 'row_count': cursor.rowcount}
        finally:
            cursor.close()
            conn.close()