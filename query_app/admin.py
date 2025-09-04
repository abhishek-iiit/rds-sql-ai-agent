from django.contrib import admin
from .models import DatabaseConnection, QueryHistory

@admin.register(DatabaseConnection)
class DatabaseConnectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'host', 'database_name', 'engine', 'user', 'created_at']
    list_filter = ['engine', 'created_at']
    search_fields = ['name', 'host', 'database_name']

@admin.register(QueryHistory)
class QueryHistoryAdmin(admin.ModelAdmin):
    list_display = ['natural_query', 'success', 'execution_time', 'user', 'created_at']
    list_filter = ['success', 'created_at']
    search_fields = ['natural_query', 'generated_sql']
    readonly_fields = ['created_at']