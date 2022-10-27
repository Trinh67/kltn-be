from config import LOGGING_CONFIG
import logging.config
from typer import Typer
from app.command.background_job import command_group as background_job_command_group

logging.config.dictConfig(LOGGING_CONFIG)

if __name__ == '__main__':
    command_root = Typer()
    command_root.add_typer(background_job_command_group, name='background-job')
    command_root()
