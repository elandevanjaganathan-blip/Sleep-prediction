from fastapi import FastAPI

app = FastAPI()

@app.get("/api/health")
@app.get("/health")
@app.get("/")
def health():
    return {"status": "healthy"}
