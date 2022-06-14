from pydantic import PydanticValueError


class NotInADefinedList(PydanticValueError):
    code = 'not_in_defined_list'
    msg_template = 'value is not in a prefix list"'


class PageInvalidError(PydanticValueError):
    code = "page_must_larger_than_0"
    msg_template = 'page must larger than 0'


class PageSizeInvalidError(PydanticValueError):
    code = "page_size_must_larger_than_0"
    msg_template = 'page size must larger than 0'


class InvalidFieldFormat(PydanticValueError):
    code = "invalid_field_format"
    msg_template = "invalid_field_format"


class InvalidField(PydanticValueError):
    code = "invalid_field"
    msg_template = "invalid field"


class ExceedMaximumArrayLength(PydanticValueError):
    code = "exceed_max_length"
    msg_template = "Array is too many elements"
