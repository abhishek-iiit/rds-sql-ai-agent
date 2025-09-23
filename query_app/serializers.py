from rest_framework import serializers
from .models import QueryHistory

class QueryRequestSerializer(serializers.Serializer):
    """Simplified query request serializer - only natural query needed."""
    natural_query = serializers.CharField(max_length=1000)

class QueryResponseSerializer(serializers.Serializer):
    """Query response serializer with results and metadata."""
    generated_sql = serializers.CharField()
    results = serializers.ListField(child=serializers.DictField(), required=False)
    execution_time = serializers.FloatField(required=False)
    error = serializers.CharField(required=False)
    columns = serializers.ListField(child=serializers.CharField(), required=False)

class QueryHistorySerializer(serializers.ModelSerializer):
    """Query history serializer for displaying past queries."""
    class Meta:
        model = QueryHistory
        fields = ['id', 'natural_query', 'generated_sql', 'execution_time', 'success', 'error_message', 'created_at']