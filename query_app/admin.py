from django.contrib import admin
from .models import QueryHistory

@admin.register(QueryHistory)
class QueryHistoryAdmin(admin.ModelAdmin):
    list_display = ['natural_query', 'success', 'execution_time', 'created_at']
    list_filter = ['success', 'created_at']
    search_fields = ['natural_query', 'generated_sql']
    readonly_fields = ['created_at']
    list_per_page = 25