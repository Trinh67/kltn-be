import logging
import docx2txt
from app.adapter.elastic import ElasticService

from app.dto.core.file import CreateFileRequest, GetFileResponse
from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class FileService:
    @classmethod
    def create_file(cls, request_input: CreateFileRequest):
        file_path = f'{DATA_PATH}/{request_input.user_id}/{request_input.file_path}'

        # extract text
        text = docx2txt.process(file_path)

        print(text)
        return {"id": 1}
    
    @classmethod
    def get_file(cls, id: int):
        data = ElasticService.get_file(id)
        print(data)
        return GetFileResponse.parse_obj(data)