import logging
from plistlib import InvalidFileException
import docx2txt
import pdfplumber
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.adapter.elastic import ElasticService
from app.dto.core.file import GetFileDBResponse, SearchFileMappingResponse

from app.dto.core.file_elastic import CreateFileRequest, CreateFileResponse, SearchFileRequest
from app.helper.constant import Constant
from app.helper.custom_exception import ElasticServiceCallException
from app.helper.paging import Pagination
from app.model.file import File
from setting import setting

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class FileElasticService:
    @classmethod
    def create_file(cls, db: Session, request_input: CreateFileRequest):
        file_path = f'{DATA_PATH}/{request_input.user_id}/{request_input.file_name}'

        try:
            if request_input.file_name.split('.')[1] in Constant.DOCX_FILE_EXT:
                # extract text from docx
                content = docx2txt.process(file_path)
                data = ElasticService.create_file(content)
            elif request_input.file_name.split('.')[1] in Constant.PDF_FILE_EXT:
                # extract text from pdf
                with pdfplumber.open(file_path) as pdf:
                    num_pages = len(pdf.pages)
                    content = ''
                    for i in range(0, num_pages):
                        page = pdf.pages[i]
                        content += page.extract_text() + f'--- page {i} ----'
                    data = ElasticService.create_file(content)
            else:
                raise InvalidFileException
            
            request_model_dict = {
                "user_id": request_input.user_id,
                "file_name": request_input.file_name,
                "category_id": request_input.category_id,
                "file_elastic_id": data.id
            }
            new_file = File.create(db, request_model_dict)
            db.commit()
        except Exception as e:
            _logger.exception(e)
            return Exception(f'Failed to create file')


        return CreateFileResponse(new_file_id = new_file.id)
    
    @classmethod
    def get_file(cls, id: str):
        data = ElasticService.get_file(id)
        return data
    
    @classmethod
    def get_list_file(cls, size: int):
        data = ElasticService.get_list_file(size)
        return data
    
    @classmethod
    def search_content(cls, db: Session, request_input: SearchFileRequest):
        filter_ids = ElasticService.search_content(request_input.content, request_input.size).files
        print(filter_ids)
        files = File.q(db, and_(File.file_elastic_id.in_(filter_ids), File.deleted_at.is_(None))) \
                    .join(File.users) \
                    .all()
        total_files = len(files)
        dto_files = []
        for file in files:
            dto_file = GetFileDBResponse(**file.to_dict(), author_name=file.users.name)
            dto_files.append(dto_file)
        return SearchFileMappingResponse(files=dto_files), Pagination(total_items=total_files, current_page=1, page_size=100)