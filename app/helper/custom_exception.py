from pydantic import BaseModel
from app.config.field_name_mapping import data_mapping


class Message(BaseModel):
    en: str
    vi: str


class CommonException(Exception):
    http_code: int
    code: int
    message: [str, Message]

    def __init__(self, http_code: int = None, code: int = None, message: [str, Message] = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else self.http_code
        self.message = message

    def __str__(self):
        return str(self.message)

class ValidateException(CommonException):
    def __init__(self, code: int = None, message: object = None):
        self.http_code = 400
        self.code = code if code else self.http_code
        self.message = message


class ExistedException(CommonException):

    def __init__(self, code: int = None, message: object = None):
        self.http_code = 409
        self.code = code if code else self.http_code
        self.message = message


class ObjectNotFound(CommonException):
    def __init__(self, obj: object = None):
        super().__init__(http_code=400, code=404, message=Message(en=f"{obj.value} not found",
                                                                  vi=f"{translate_message(obj.value, 'vi')} không tồn tại"))


class URLNotFound(CommonException):
    def __init__(self, obj: object = None):
        super().__init__(http_code=404, code=404, message=Message(en=f"{obj.value} not found",
                                                                  vi=f"{translate_message(obj.value, 'vi')} không tồn tại"))


class InternalServerError(CommonException):
    def __init__(self):
        super().__init__(http_code=500, code=500, message=Message(en="Internal server error",
                                                                  vi="Lỗi hệ thống"))


class FieldIsRequired(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=402, message=Message(en=f"{field_name} is required",
                                                                  vi=f"{translate_message(field_name, 'vi')} bắt buộc phải nhập"))


class InvalidFileFormat(CommonException):
    def __init__(self):
        super().__init__(http_code=400, code=415, message=Message(en="File format is invalid",
                                                                  vi="Định dạng tệp không hợp lệ"))


class InvalidField(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=420, message=Message(en=f"{field_name} is invalid",
                                                                  vi=f"{translate_message(field_name, 'vi')} không hợp lệ"))


class InvalidFieldFormat(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=417, message=Message(en=f"{field_name} format is invalid",
                                                                  vi=f"{translate_message(field_name, 'vi')} có định dạng không hợp lệ"))


class NotInDefinedList(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=414, message=Message(en=f"{field_name} not in a defined list",
                                                                  vi=f"{translate_message(field_name, 'vi')} không có trong danh sách xác định"))


class FieldDuplicated(CommonException):
    def __init__(self, field_name: str):
        super().__init__(http_code=400, code=421, message=Message(en=f"{field_name} is duplicated",
                                                                  vi=f"{translate_message(field_name, 'vi')} không được phép trùng nhau"))


class PermissionDenied(CommonException):
    def __init__(self):
        super().__init__(http_code=403, code=403, message=Message(en="Permission denied",
                                                                  vi="Không có quyền truy cập"))


class Unauthorized(CommonException):
    def __init__(self):
        super().__init__(http_code=401, code=401, message=Message(en="Unauthorized",
                                                                  vi="Không được phép"))


def translate_message(field_name: str, lang: str) -> str:
    if data_mapping[lang].get(field_name):
        return data_mapping[lang][field_name]
    return field_name
