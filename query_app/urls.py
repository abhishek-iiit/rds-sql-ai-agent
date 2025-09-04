from django.urls import path
from . import views

urlpatterns = [
    path('connections/', views.list_database_connections, name='list_connections'),
    path('connections/create/', views.create_database_connection, name='create_connection'),
    path('connections/<int:connection_id>/schema/', views.get_database_schema, name='get_schema'),
    path('query/', views.execute_natural_query, name='execute_query'),
    path('history/', views.get_query_history, name='query_history'),
]