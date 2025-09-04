from django.db import models
from django.contrib.auth.models import User

class DatabaseConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    host = models.CharField(max_length=255)
    port = models.IntegerField(default=5432)
    database_name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)  # Encrypted in production
    engine = models.CharField(max_length=20, choices=[
        ('postgresql', 'PostgreSQL'),
        ('mysql', 'MySQL'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'name']

class QueryHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    database_connection = models.ForeignKey(DatabaseConnection, on_delete=models.CASCADE)
    natural_query = models.TextField()
    generated_sql = models.TextField()
    execution_time = models.FloatField(null=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)