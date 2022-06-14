import logging.config
import uvicorn
from app import create_app
from config import LOGGING_CONFIG

logging.config.dictConfig(LOGGING_CONFIG)

app = create_app()

if __name__ == '__main__':
    uvicorn.run("main:app", port=5002, reload=True, access_log=False)
