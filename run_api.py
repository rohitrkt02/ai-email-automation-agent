import uvicorn

if __name__ == "__main__":
    print("[SYSTEM] Launching FastAPI REST API Gateway on http://127.0.0.1:8000")
    print("[SYSTEM] Open http://127.0.0.1:8000/docs for Swagger UI Dashboard Interactive Testing\n")
    uvicorn.run("app.main_api:app", host="127.0.0.1", port=8000, reload=True)