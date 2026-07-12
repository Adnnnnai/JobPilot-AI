from fastapi import FastAPI

app = FastAPI(
    title="JobPilot AI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "JobPilot AI Backend Running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }
