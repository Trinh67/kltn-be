from sqlalchemy.orm import Session
from app.model.file import File


class FileProvider:
    @classmethod
    def create_file_model(cls, db: Session, commit: bool = False, **data) -> File:
        file = {
            'id': data.get('id', 1),
            "user_id": data.get("user_id", "123456789"),
            "category_id": data.get("category_id", 1),
            "file_name": data.get("file_name", "test.pdf"),
            "file_description": data.get("file_description", "file demo"),
            "pages": data.get("pages", 10),
            "downloads": data.get("downloads", 2),
            "file_elastic_id": data.get("file_elastic_id", None),
            'file_title': data.get('file_title', "file demo"),
            'google_driver_id': data.get('google_driver_id', None),
            'status': data.get('status', 0),
            'refuse_reason': data.get('refuse_reason', None)
        }

        new_file: File = File.create(db, file, commit=commit)

        return new_file

