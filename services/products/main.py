from fastapi import FastAPI

app = FastAPI(title="Products Service")

@app.get("/health")
def health():
    return {"status": "ok", "service": "products"}
