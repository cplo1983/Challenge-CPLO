from sqlalchemy import Column, Integer, String, UniqueConstraint
from app.database import Base

class RemediatedCVE(Base):
    __tablename__ = "remediated_cves"
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_id = Column(String, nullable=False)
    cve_id = Column(String, nullable=False)
    __table_args__ = (UniqueConstraint('team_id', 'cve_id', name='_team_cve_uc'),)