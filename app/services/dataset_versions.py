from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
import pandas as pd
from app.core.config import settings

def persist_dataset(raw_bytes:bytes, filename:str, valid:pd.DataFrame, rejected:pd.DataFrame, mapping:dict, quality:dict, tenant_id="demo-store"):
    checksum=hashlib.sha256(raw_bytes).hexdigest(); version=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+checksum[:8]
    root=Path(settings.upload_root)/tenant_id/version; root.mkdir(parents=True,exist_ok=True)
    safe=Path(filename).name; (root/("raw_"+safe)).write_bytes(raw_bytes)
    valid.to_csv(root/"validated.csv",index=False); rejected.to_csv(root/"rejected.csv",index=False)
    manifest={"version":version,"filename":safe,"checksum":checksum,"created_at":datetime.now(timezone.utc).isoformat(),"mapping":mapping,"quality":quality,"valid_rows":len(valid),"rejected_rows":len(rejected)}
    (root/"manifest.json").write_text(json.dumps(manifest,indent=2,default=str),encoding="utf-8")
    return manifest
