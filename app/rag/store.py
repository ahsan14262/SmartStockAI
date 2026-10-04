import json, pickle
from pathlib import Path
import numpy as np
from app.core.config import settings
class HybridStore:
    def __init__(self,tenant_id,corpus_id="business",version="v1"):
        self.dir=Path(settings.vectorstore_root)/tenant_id/corpus_id/version
        self.dir.mkdir(parents=True,exist_ok=True)
        self.chunks=[]; self.meta=[]; self.index=None; self.bm25=None; self.model=None
    def build(self,chunks,metadata):
        from sentence_transformers import SentenceTransformer
        from rank_bm25 import BM25Okapi
        import faiss
        self.model=SentenceTransformer(settings.embedding_model)
        emb=self.model.encode(chunks,normalize_embeddings=True,show_progress_bar=False).astype("float32")
        self.index=faiss.IndexFlatIP(emb.shape[1]); self.index.add(emb)
        self.chunks=chunks; self.meta=metadata
        self.bm25=BM25Okapi([c.lower().split() for c in chunks])
        faiss.write_index(self.index,str(self.dir/"index.faiss"))
        (self.dir/"chunks.json").write_text(json.dumps({"chunks":chunks,"metadata":metadata},ensure_ascii=False),encoding="utf-8")
        with open(self.dir/"bm25.pkl","wb") as f: pickle.dump(self.bm25,f)
        (self.dir/"manifest.json").write_text(json.dumps({"embedding_model":settings.embedding_model,"count":len(chunks)},indent=2))
    def load(self):
        import faiss
        from sentence_transformers import SentenceTransformer
        self.model=SentenceTransformer(settings.embedding_model)
        self.index=faiss.read_index(str(self.dir/"index.faiss"))
        data=json.loads((self.dir/"chunks.json").read_text(encoding="utf-8"))
        self.chunks,self.meta=data["chunks"],data["metadata"]
        with open(self.dir/"bm25.pkl","rb") as f: self.bm25=pickle.load(f)
    def search(self,query,k=5):
        if self.index is None: self.load()
        q=self.model.encode([query],normalize_embeddings=True).astype("float32")
        _,ids=self.index.search(q,min(k*3,len(self.chunks)))
        dense=[int(i) for i in ids[0] if i>=0]
        sparse=np.argsort(self.bm25.get_scores(query.lower().split()))[::-1][:k*3].tolist()
        scores={}
        for rank,i in enumerate(dense): scores[i]=scores.get(i,0)+1/(60+rank+1)
        for rank,i in enumerate(sparse): scores[i]=scores.get(i,0)+1/(60+rank+1)
        ranked=sorted(scores,key=scores.get,reverse=True)[:k]
        return [{"text":self.chunks[i],"metadata":self.meta[i],"score":scores[i]} for i in ranked]
