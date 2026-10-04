from app.db.session import SessionLocal
from app.db.models import AuditLog
def audit(tenant_id,actor,action,detail=""):
    with SessionLocal() as db:
        db.add(AuditLog(tenant_id=tenant_id,actor=actor,action=action,detail=detail[:4000]))
        db.commit()
