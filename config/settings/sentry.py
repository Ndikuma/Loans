import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Initialize Sentry SDK
sentry_sdk.init(
    dsn="https://f0cce249c8377f34954dd6d86d6458d3@o4508643256500224.ingest.us.sentry.io/4508643258073088",
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,  # Adjust the sample rate (1.0 captures all traces, lower for less)
    send_default_pii=True,  # Send user information (e.g., emails) with errors
)
