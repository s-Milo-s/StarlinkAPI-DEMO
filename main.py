"""
Application entrypoint
"""
import uvicorn
from app.main import create_app
from app.core.config import SERVER_HOST, SERVER_PORT

app = create_app()

if __name__ == "__main__":
    uvicorn.run(app, host=SERVER_HOST, port=SERVER_PORT)
