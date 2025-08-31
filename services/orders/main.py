from fastapi import FastAPI

app = FastAPI(title="Orders Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "orders"}
