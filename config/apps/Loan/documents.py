# documents.py

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from .models import Loan, Wallet, WalletActivity


@registry.register_document
class LoanDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = "loans"
        # Do not specify shards or replicas for serverless Elasticsearch
        settings = {}

    class Django:
        model = Loan  # The model associated with this Document
        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            "amount",
            "interest_rate",
            "status",
            "description",
            "penalty_rate",
        ]


@registry.register_document
class WalletDocument(Document):
    class Index:
        name = "wallets"
        settings = {}

    class Django:
        model = Wallet
        fields = [
            "wallet_type",
            "balance",
            "notifications_enabled",
        ]


@registry.register_document
class WalletActivityDocument(Document):
    class Index:
        name = "wallet_activities"
        settings = {}

    class Django:
        model = WalletActivity
        fields = [
            "activity_type",
            "amount",
            "timestamp",
        ]
