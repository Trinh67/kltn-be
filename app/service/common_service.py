import logging
import shutil
import traceback
from io import BytesIO
import os

from app.helper.custom_exception import InternalServerError, ObjectNotFound
from app.helper.exception_handler import CommonException, Message, ValidateException
from app.util.common import generate_unique_filename
from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

def upload_file(user_id, file):
    try:
        filename = file.filename

        # save file in local
        folder_path = f'{DATA_PATH}/{user_id}'
        isFolderExist = os.path.exists(folder_path)
        if not isFolderExist:
            os.makedirs(folder_path)

        file_name = generate_unique_filename(filename)
        file_path = f'{DATA_PATH}/{user_id}/{file_name}'
        isFileExist = os.path.exists(file_path)
        if isFileExist:
            raise ValidateException(410, Message(en = 'File name is exist', \
                                                 vi = 'Tên tệp đã tồn tại'))
        with open(file_path, 'wb') as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"file_name": file_name}
    except CommonException as e:
            raise e
    except Exception as e:
        _logger.error(f"____error: {str(e)} when process transaction result.")
        traceback.print_exc()
        raise InternalServerError()


def download_file(file_path: str):
    try:
        # get file
        file = object
        return file
    except ObjectNotFound as e:
        raise e
    except Exception as e:
        _logger.error(f"____error: {str(e)} when process transaction result.")
        traceback.print_exc()
        raise InternalServerError()
