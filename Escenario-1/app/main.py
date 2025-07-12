from fastapi import FastAPI, Depends, HTTPException, Header, status
from app.nist_client import get_nist_summary, get_cve_by_id
from app.database import SessionLocal, engine, Base, get_db
from app.models import RemediatedCVE
from app.schemas import RemediateRequest, SummaryResponse
from app.auth import verify_api_key
import logging

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/vulnerabilities/summary", response_model=SummaryResponse)
def get_vuln_summary(api_key: str = Depends(verify_api_key)):
    return get_nist_summary()

@app.post("/remediated", status_code=201)
def remediate_vuln(rem: RemediateRequest, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    # Verificamos que el CVE exista en NIST
    cve = get_cve_by_id(rem.cve_id)
    if not cve:
        raise HTTPException(status_code=404, detail="CVE not found in NIST")
    # Guardamos remediación
    obj = RemediatedCVE(team_id=rem.team_id, cve_id=rem.cve_id)
    db.add(obj)
    db.commit()
    logging.info(f"Remediated CVE {rem.cve_id} for team {rem.team_id}")
    return {"message": "Remediation saved"}

@app.get("/vulnerabilities/summary/unremediated", response_model=SummaryResponse)
def get_unremediated(team_id: str, db=Depends(get_db), api_key: str = Depends(verify_api_key)):
    remediated_cves = db.query(RemediatedCVE.cve_id).filter_by(team_id=team_id).all()
    remediated_set = set([r[0] for r in remediated_cves])
    summary = get_nist_summary(exclude_cves=remediated_set)
    return summary