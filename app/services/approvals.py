from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import hashlib,json,uuid
@dataclass
class Proposal:
    id:str; kind:str; payload:dict; input_hash:str; status:str="pending"; created_at:str=""

def create_proposal(kind,payload,material_inputs):
    raw=json.dumps(material_inputs,sort_keys=True,default=str).encode(); h=hashlib.sha256(raw).hexdigest()
    return asdict(Proposal(str(uuid.uuid4()),kind,payload,h,"pending",datetime.now(timezone.utc).isoformat()))
def approve(proposal,actor,current_material_inputs):
    h=hashlib.sha256(json.dumps(current_material_inputs,sort_keys=True,default=str).encode()).hexdigest()
    if h!=proposal["input_hash"]: raise ValueError("Material inputs changed; approval must be requested again.")
    proposal.update(status="approved",approved_by=actor,approved_at=datetime.now(timezone.utc).isoformat()); return proposal
