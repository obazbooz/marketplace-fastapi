from fastapi import FastAPI

app = FastAPI(title="Marketplace API")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Marketplace API"}