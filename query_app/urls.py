from django.urls import path
from .views import SchemaView, QueryView, HistoryView, ClearHistoryView

urlpatterns = [
    path('schema/', SchemaView.as_view(), name='get_schema'),
    path('query/', QueryView.as_view(), name='execute_query'),
    path('history/', HistoryView.as_view(), name='query_history'),
    path('history/clear/', ClearHistoryView.as_view(), name='clear_query_history'),
]