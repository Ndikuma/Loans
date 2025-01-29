from django.http import JsonResponse

from .utils.elasticsearch_client import create_index_with_mappings

# Create your views here.
# search/views.py


def create_index(request):
    """
    View to create an index in Elasticsearch with mappings.
    """
    try:
        mapping_response = create_index_with_mappings()
        return JsonResponse(
            {"message": "Index created successfully", "response": mapping_response}
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
