from fastapi import FastAPI

app = FastAPI(title="Candidate Processor BTG")


@app.get("/")
def home():
    return {"mensagem:": "Hello word"}


@app.post("/jobs")
def upload():
    return {"message": "upload"}
