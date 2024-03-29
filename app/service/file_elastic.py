import logging
import docx2txt
import pdfplumber
from docx2pdf import convert
from sqlalchemy import and_
from sqlalchemy.orm import Session
from app.adapter.elastic import ElasticService
from app.dto.core.file import GetFileDBResponse, SearchFileMappingResponse
from app.helper.enum import FileStatus

from setting import setting
from app.model.file import File
from app.helper.constant import Constant
from app.helper.paging import Pagination
from app.helper.custom_exception import ElasticServiceCallException, InvalidFileFormat
from app.dto.core.file_elastic import CreateFileRequest, CreateFileResponse, SearchFileRequest

_logger = logging.getLogger(__name__)

DATA_PATH = setting.DATA_STORAGE

class FileElasticService:
    @classmethod
    def create_file(cls, db: Session, request_input: CreateFileRequest, user_id: int):
        try:
            # if request_input.file_path.split('.')[1] in Constant.DOCX_FILE_EXT:
            #     # extract text from docx
            #     # pdf_file = f'{DATA_PATH}/convert/output.pdf'
            #     # convert(file_path, pdf_file)
            #     # with pdfplumber.open(pdf_file) as pdf:
            #     #     num_pages = len(pdf.pages)
            #     content = docx2txt.process(file_path)
            #     data = ElasticService.create_file(content)
            # elif request_input.file_path.split('.')[1] in Constant.PDF_FILE_EXT:
            #     # extract text from pdf
            #     with pdfplumber.open(file_path) as pdf:
            #         num_pages = len(pdf.pages)
            #         content = ''
            #         for i in range(0, num_pages):
            #             page = pdf.pages[i]
            #             content += page.extract_text() + f'--- page {i} ----'
            #         data = ElasticService.create_file(content)
            # else:
            #     raise InvalidFileFormat
            
            request_model_dict = {
                "user_id": user_id,
                "file_name": request_input.file_path,
                "file_title": request_input.file_title,
                "file_description": request_input.file_description,
                "category_id": request_input.category_id,
                "file_elastic_id": None,
                "pages": None,
                "status": FileStatus.PROCESSING.value
            }
            new_file = File.create(db, request_model_dict)
            db.commit()
        except Exception as e:
            _logger.exception(e)
            raise ElasticServiceCallException('api create new file')


        return CreateFileResponse(new_file_id = new_file.id)
    
    @classmethod
    def search_content(cls, db: Session, request_input: SearchFileRequest):
        filter_ids = ElasticService.search_content(request_input.content, request_input.size).files
        files = db.query(File) \
                .filter(File.file_elastic_id.in_(filter_ids), File.status == FileStatus.APPROVED.value, File.deleted_at.is_(None)) \
                .all()
        total_files = len(files)
        dto_files = []
        for id in filter_ids:
            for file in files:
                if file.file_elastic_id == id:
                    file_path = f"{file.user_id}/{file.file_name}"
                    dto_file = GetFileDBResponse(**file.to_dict(), file_path=file_path, author_name=file.users.name, \
                                                 category_vi=file.categories.name_vi, category_en=file.categories.name_en)
                    dto_files.append(dto_file)
                    break
        return SearchFileMappingResponse(files=dto_files), Pagination(total_items=total_files, current_page=1, page_size=100)