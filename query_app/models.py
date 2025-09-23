from django.db import models

class QueryHistory(models.Model):
    """Simplified query history model without user/connection dependencies."""
    natural_query = models.TextField()
    generated_sql = models.TextField()
    execution_time = models.FloatField(null=True)
    success = models.BooleanField(default=False)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Query History'
        verbose_name_plural = 'Query Histories'