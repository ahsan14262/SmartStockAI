from dataclasses import dataclass, field
from datetime import datetime
import uuid
@dataclass
class Job:
    kind:str
    tenant_id:str
    id:str=field(default_factory=lambda:str(uuid.uuid4()))
    status:str="queued"
    created_at:str=field(default_factory=lambda:datetime.utcnow().isoformat())
# Production recommendation: replace this scaffold with a durable queue (e.g. Celery/RQ/Dramatiq)
# backed by Redis/PostgreSQL, with idempotency keys, retries, cancellation and persisted status.
