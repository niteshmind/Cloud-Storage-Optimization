"""Prometheus metrics configuration."""

from prometheus_client import Counter, Histogram, Info, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

from app.core.config import settings

# Application info
app_info = Info("costintel_app", "Application information")
app_info.info({
    "version": settings.APP_VERSION,
    "environment": settings.APP_ENVIRONMENT,
})

# Request metrics
request_count = Counter(
    "costintel_requests_total",
    "Total requests",
    ["method", "endpoint", "status"]
)

request_duration = Histogram(
    "costintel_request_duration_seconds",
    "Request duration",
    ["method", "endpoint"],
    buckets=[0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 30.0]
)

# Business metrics
ingestion_jobs = Counter(
    "costintel_ingestion_jobs_total",
    "Total ingestion jobs",
    ["status"]
)

classification_jobs = Counter(
    "costintel_classification_jobs_total",
    "Total classification jobs",
    ["status", "category"]
)

webhook_deliveries = Counter(
    "costintel_webhook_deliveries_total",
    "Total webhook deliveries",
    ["status"]
)


def get_metrics_response() -> Response:
    """Generate Prometheus metrics response."""
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
