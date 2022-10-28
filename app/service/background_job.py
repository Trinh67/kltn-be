import logging
import docx2txt
import pdfplumber

from sqlalchemy import and_, desc, or_
from sqlalchemy.orm import Session
from app.adapter.elastic import ElasticService
from app.helper.constant import Constant
from app.helper.custom_exception import ElasticServiceCallException, InvalidFileFormat
from app.helper.enum import FileStatus

from app.model.file import File
from app.service.file_elastic import DATA_PATH
from setting import setting

_logger = logging.getLogger(__name__)

class BackgroundJobService:
    @classmethod
    def upload_file_to_elastic_search(cls, db: Session):
        _logger.info('Stating job upload file to Elastic')
        list_file = File.q(db, File.status == FileStatus.PROCESSING, File.deleted_at.is_(None))
        list_id = [file.id for file in list_file]
        _logger.info(f'Start up load {len(list_id)} files')
        try:
            data = {}
            for file in list_file:
                num_pages = 0
                file_path = f'{DATA_PATH}/{file.user_id}/{file.file_name}'
                if file.file_name.split('.')[1] in Constant.DOCX_FILE_EXT:
                    # extract text from docx
                    # pdf_file = f'{DATA_PATH}/convert/output.pdf'
                    # convert(file_path, pdf_file)
                    # with pdfplumber.open(pdf_file) as pdf:
                    #     num_pages = len(pdf.pages)
                    content = docx2txt.process(file_path)
                    data = ElasticService.create_file(content)
                elif file.file_name.split('.')[1] in Constant.PDF_FILE_EXT:
                    # extract text from pdf
                    with pdfplumber.open(file_path) as pdf:
                        num_pages = len(pdf.pages)
                        content = ''
                        for i in range(0, num_pages):
                            page = pdf.pages[i]
                            content += page.extract_text() + f'--- page {i} ----'
                        data = ElasticService.create_file(content)
                else:
                    raise InvalidFileFormat
            if data:
                request_model_dict = {
                    "file_elastic_id": data.id,
                    "pages": num_pages,
                    "status": FileStatus.DRAFT.value
                }
                db.query(File).filter(File.id == file.id).update(request_model_dict)
                db.commit()
        except Exception as e:
            _logger.exception(e)
            # raise ElasticServiceCallException('api create new file')

        _logger.info('Finish job upload file to Elastic')
        
        return
