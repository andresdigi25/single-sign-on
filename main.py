#export config_secret_manager=dev/sso-api && python main.py
#export config_secret_manager=dev/sso-api && uvicorn app.api:app --host 0.0.0.0 --port 8000 --workers 4

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.api:app", host="0.0.0.0", port=8000,workers =4,reload=False)
