import uvicorn
from main import app
if __name__ == "__main__":
    # uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug",
    #             workers=1, limit_concurrency=1, limit_max_requests=1)
    if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")