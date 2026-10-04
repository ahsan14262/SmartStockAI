from sqlalchemy import String, Integer, Float, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.db.session import Base

class AuditLog(Base):
    __tablename__="audit_logs"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    tenant_id:Mapped[str]=mapped_column(String(64),index=True)
    actor:Mapped[str]=mapped_column(String(200))
    action:Mapped[str]=mapped_column(String(100))
    detail:Mapped[str]=mapped_column(Text,default="")
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class DatasetVersion(Base):
    __tablename__="dataset_versions"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    tenant_id:Mapped[str]=mapped_column(String(64),index=True)
    filename:Mapped[str]=mapped_column(String(255))
    checksum:Mapped[str]=mapped_column(String(64),index=True)
    rows:Mapped[int]=mapped_column(Integer)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)

class Approval(Base):
    __tablename__="approvals"
    id:Mapped[int]=mapped_column(Integer,primary_key=True)
    tenant_id:Mapped[str]=mapped_column(String(64),index=True)
    kind:Mapped[str]=mapped_column(String(80))
    payload:Mapped[str]=mapped_column(Text)
    status:Mapped[str]=mapped_column(String(30),default="pending")
    approved_by:Mapped[str|None]=mapped_column(String(200),nullable=True)
    created_at:Mapped[datetime]=mapped_column(DateTime,default=datetime.utcnow)
