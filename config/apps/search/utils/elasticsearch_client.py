# search/utils/elasticsearch_client.py

from django.conf import settings
from elasticsearch import Elasticsearch


def get_elasticsearch_client():
    """
    This function returns an Elasticsearch client configured with the API key.
    """
    client = Elasticsearch(
        settings.ELASTICSEARCH_DSL["default"]["hosts"],
        api_key=settings.ELASTICSEARCH_DSL["default"]["api_key"],
    )
    return client


def create_index_with_mappings():
    """
    This function creates an index with the provided mappings in Elasticsearch.
    It does not include settings for shards or replicas to support serverless mode.
    """
    client = get_elasticsearch_client()

    index_name = "search-imb5"
    mappings = {"properties": {"text": {"type": "text"}}}

    # Create the index with mappings (without settings for shards or replicas)
    index_exists = client.indices.exists(index=index_name)
    if not index_exists:
        create_response = client.indices.create(
            index=index_name,
            body={"mappings": mappings},  # Do not include shards/replicas
        )
        return create_response
    else:
        return {"message": "Index already exists"}
