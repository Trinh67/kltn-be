import logging
import time

from typer import Typer
from app.service.background_job import BackgroundJobService
from setting import setting

from app.helper.db import db_session

command_group = Typer()
_logger = logging.getLogger(__name__)

@command_group.command(help='upload file to Elastic Search service')
def upload_file_to_elastic_search():
    with next(db_session()) as db:
        while True:
            BackgroundJobService.upload_file_to_elastic_search(db=db)
            db.rollback()
            time.sleep(setting.UPLOAD_FILE_ELASTIC_SEARCH_SLEEP_TIME)