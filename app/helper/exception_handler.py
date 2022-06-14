from fastapi import Request, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from app.helper.custom_errors import PageInvalidError, PageSizeInvalidError, NotInADefinedList, InvalidFieldFormat, \
    InvalidField, ExceedMaximumArrayLength
from app.helper.base_response import ResponseSchemaBase
from app.helper.custom_exception import CommonException, InternalServerError, Message, translate_message


async def base_exception_handler(request: Request, exc: CommonException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, exc.message))
    )


async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.status_code, exc.detail))
    )


async def validation_exception_handler(request, exc):
    code, msg = request_get_message_validation(exc)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(code, msg))
    )


async def request_validation_exception_handler(request, exc):
    code, msg = request_get_message_validation(exc)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(code, msg))
    )


async def fastapi_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            ResponseSchemaBase().custom_response(InternalServerError().code, InternalServerError().message)
        )
    )


def get_message_validation(exc):
    print(exc.errors())
    messages = ["/'{}'/: {}".format(error.get("loc")[len(error.get("loc")) - 1], error.get("msg")) for error in
                exc.errors()]
    return ', '.join(messages)


def request_get_message_validation(exc) -> (int, object):
    # print(json.dumps(exc.errors(), indent=2))
    print(exc.errors())
    types = [error.get('type') for error in exc.errors()]
    messages = [error.get("loc")[len(error.get("loc")) - 1] for error in exc.errors()]
    limit_value = [error.get('ctx').get('limit_value') if error.get('ctx') else '' for error in exc.errors()]
    for err_type, msg, limit in zip(types, messages, limit_value):
        if err_type == "value_error.missing":
            return 402, Message(en=f"Param {msg} is required", \
                                vi=f"Tham số {translate_message(msg, 'vi')} bắt buộc nhập")
        elif err_type == "value_error.any_str.min_length":
            return 412, Message(en=f"{msg} must have at least {limit} characters", \
                                vi=f"{translate_message(msg, 'vi')} phải là chuỗi dài tối thiểu {limit} ký tự")
        elif err_type == "value_error.any_str.max_length":
            return 411, Message(en=f"{msg} must have at most {limit} characters", \
                                vi=f"{translate_message(msg, 'vi')} phải là chuỗi dài tối đa {limit} ký tự")
        elif err_type in [f"value_error.{NotInADefinedList.code}", "type_error.enum"]:
            return 414, Message(en=f"Param {msg} is not in defined values", \
                                vi=f"Tham số {translate_message(msg, 'vi')} không có trong danh sách xác định")
        elif err_type == f"value_error.{PageInvalidError.code}":
            return 406, Message(en="Page number is invalid", \
                                vi="Số trang không hợp lệ")
        elif err_type == f"value_error.{PageSizeInvalidError.code}":
            return 407, Message(en="Page size is invalid", \
                                vi="Kích thước trang không hợp lệ")
        elif err_type == f"value_error.{ExceedMaximumArrayLength.code}":
            return 411, Message(en=f"Param {msg} is too long", \
                                vi=f"Tham số {translate_message(msg, 'vi')} quá dài")
        elif err_type == "value_error.jsondecode":
            return 400, Message(en="Invalid json body", \
                                vi="Nội dung json không hợp lệ")
        elif err_type == "value_error.number.not_le" or err_type == "value_error.number.not_lt":
            return 418, Message(en=f"{msg} is too large", \
                                vi=f"{translate_message(msg, 'vi')} có giá trị quá lớn")
        elif err_type == "value_error.number.not_ge" or err_type == "value_error.number.not_gt":
            return 419, Message(en=f"{msg} is too small", \
                                vi=f"{translate_message(msg, 'vi')} có giá trị quá nhỏ")
        elif err_type in ["type_error.number", "type_error.str", "type_error.string", "type_error.list",
                          "type_error.integer",
                          "type_error.bool"] \
                or err_type == f"value_error.{InvalidFieldFormat.code}":
            return 417, Message(en=f"{msg} format is invalid", \
                                vi=f"{translate_message(msg, 'vi')} có định dạng không hợp lệ")
        elif err_type == InvalidField.code:
            return 420, Message(en=f"{msg} is invalid", \
                                vi=f"{translate_message(msg, 'vi')} không hợp lệ")

    return 420, Message(en=f"{msg} is invalid", \
                        vi=f"{translate_message(msg, 'vi')} không hợp lệ")


def remove_all_open_api_422(app: FastAPI) -> None:
    paths = app.openapi().get("paths")
    for path, operations in paths.items():
        for method, metadata in operations.items():
            metadata["responses"].pop("422", None)
