import hashlib, hmac, re
from pathlib import Path

ROLES = {
 "owner":{"dashboard","upload","forecast","inventory","chat","customers","market","pricing","finance","hr","reports","approvals","settings"},
 "manager":{"dashboard","upload","forecast","inventory","chat","customers","market","pricing","reports","approvals"},
 "inventory":{"dashboard","upload","forecast","inventory","chat","reports"},
 "sales":{"dashboard","upload","chat","customers","pricing"},
 "finance":{"dashboard","chat","finance","reports"},
 "hr":{"dashboard","chat","hr"},
 "analyst":{"dashboard","upload","forecast","inventory","chat","customers","market","reports"},
}
def hash_password(password:str)->str:
    return hashlib.sha256(password.encode()).hexdigest()
def verify_password(password, digest): return hmac.compare_digest(hash_password(password), digest)
def allowed(role, permission): return permission in ROLES.get(role,set())
def safe_filename(name):
    name = Path(name).name
    return re.sub(r"[^A-Za-z0-9._-]","_",name)[:120]
def neutralize_spreadsheet_formula(v):
    if isinstance(v,str) and v.startswith(("=","+","-","@")): return "'"+v
    return v
