from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import QueryHistory
from .serializers import QueryRequestSerializer, QueryResponseSerializer, QueryHistorySerializer
from .services import QueryService, ErrorHandler, ResponseBuilder


class SchemaView(APIView):
    """CBV: Get database schema using environment configuration."""

    def get(self, request):
        try:
            query_service = QueryService()
            schema_info = query_service.get_database_schema()
            return Response(ResponseBuilder.success_response(schema_info, "Schema retrieved successfully"))
        except Exception as e:
            error_info = ErrorHandler.handle_query_error(e, "schema_request")
            return Response(
                ResponseBuilder.error_response(error_info['error_message']),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class QueryView(APIView):
    """CBV: Execute natural language query using environment configuration."""

    def post(self, request):
        serializer = QueryRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        natural_query = serializer.validated_data['natural_query']
        query_service = QueryService()

        try:
            query_data = query_service.execute_natural_query(natural_query)
            query_service.save_query_to_history(
                natural_query=natural_query,
                sql_query=query_data['generated_sql'],
                execution_time=query_data['execution_time'],
                success=True,
            )
            return Response(QueryResponseSerializer(query_data).data)
        except Exception as e:
            try:
                query_service.save_query_to_history(
                    natural_query=natural_query,
                    sql_query='',
                    execution_time=0,
                    success=False,
                    error_message=str(e),
                )
            except:
                pass

            error_info = ErrorHandler.handle_query_error(e, natural_query)
            return Response(
                ResponseBuilder.error_response(error_info['error_message']),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class HistoryView(APIView):
    """CBV: Get query history using service layer. Returns a plain list."""

    def get(self, request):
        try:
            query_service = QueryService()
            history = query_service.get_query_history()
            serializer = QueryHistorySerializer(history, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_info = ErrorHandler.handle_query_error(e, "history_request")
            return Response(
                ResponseBuilder.error_response(error_info['error_message']),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ClearHistoryView(APIView):
    """CBV: Delete all query history entries."""

    def delete(self, request):
        try:
            QueryHistory.objects.all().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            error_info = ErrorHandler.handle_query_error(e, "clear_history_request")
            return Response(
                ResponseBuilder.error_response(error_info['error_message']),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )