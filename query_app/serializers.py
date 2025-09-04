from rest_framework import serializers
from .models import DatabaseConnection, QueryHistory

class DatabaseConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ['id', 'name', 'host', 'port', 'database_name', 'username', 'engine', 'created_at']
        read_only_fields = ['id', 'created_at']

class DatabaseConnectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DatabaseConnection
        fields = ['name', 'host', 'port', 'database_name', 'username', 'password', 'engine']

class QueryRequestSerializer(serializers.Serializer):
    natural_query = serializers.CharField(max_length=1000)
    database_connection_id = serializers.IntegerField()
    openai_api_key = serializers.CharField(max_length=200)

class QueryResponseSerializer(serializers.Serializer):
    generated_sql = serializers.CharField()
    results = serializers.ListField(child=serializers.DictField(), required=False)
    execution_time = serializers.FloatField(required=False)
    error = serializers.CharField(required=False)
    columns = serializers.ListField(child=serializers.CharField(), required=False)

class QueryHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QueryHistory
        fields = ['id', 'natural_query', 'generated_sql', 'execution_time', 'success', 'error_message', 'created_at']