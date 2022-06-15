import operator
import os
import pytz
import re
import time

from slugify import slugify
from datetime import datetime, timedelta
from typing import Optional


def compare(inp, relate, cut) -> bool:
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq}
    return ops[relate](inp, cut)


def convert_localtime_to_utc(dt: datetime) -> datetime:
    return dt.astimezone(pytz.utc)


def is_phone_number_valid(phone_number: str):
    if not phone_number:
        return False

    is_valid_format = bool(re.match(pattern='^(0|84)?[0-9]{9}$', string=phone_number))
    if is_valid_format:
        try:
            normalize_phone_number(phone_number, raise_error=True)
            return True
        except Exception:
            return False
    return False


def normalize_phone_number(phone_number, prefix='84', raise_error=True):
    """
    Convert all format phone number to prefix+xxx
    :param raise_error:
    :param str phone_number:
    :param str prefix:
    :return:
    """
    # phone = re.search('^(\+84|84|0084|0)(?P<phone>\d{9}$)', phone_number.strip())
    if phone_number:
        phone = ''.join([c for c in phone_number if c.isdigit()])
        if len(phone) >= 9:
            head = phone[:-9]
            tail = phone[-9:]
            if head in ['84', '0084', '0', '']:
                if tail[0] in '35789':
                    return prefix + tail
    if raise_error:
        raise Exception(f'Have phone number invalid format: `{phone_number}`')
    return phone_number


def parse_apply_from_date_from_file(
        apply_from_date_str: Optional[str],
        local_tz=None,
        raise_error=True
):
    if not apply_from_date_str:
        return None

    try:
        return pytz.timezone('Asia/Ho_Chi_Minh') \
            .localize(datetime.strptime(apply_from_date_str, '%d/%m/%Y %H:%M:%S')) \
            .astimezone(tz=local_tz) \
            .replace(tzinfo=None)
    except ValueError:
        if not raise_error:
            return None

        raise ValueError('Invalid apply_from_date format')


def end_of_day(dt: datetime):
    return dt.astimezone(pytz.timezone('Asia/Ho_Chi_Minh')) \
        .replace(hour=23, minute=59, second=59, microsecond=0) \
        .astimezone() \
        .replace(tzinfo=None)


def split_into_new_update_remove_list(new_list: list, old_list: list) -> (list, list, list):
    new, update, remove = [], [], []
    for new_obj in new_list:
        if new_obj not in old_list:
            new.append(new_obj)
        else:
            update.append(new_obj)

    for old_obj in old_list:
        if old_obj not in new_list:
            remove.append(old_obj)

    return new, update, remove


def ceil_datetime_by_hour(dt: datetime):
    return dt + (datetime.min - dt) % timedelta(hours=1)


def floor_datetime_by_hour(dt: datetime):
    return dt.replace(minute=0, second=0, microsecond=0)


def paginate(data, page, page_size):
    paginated_data = [data[i: i + page_size] for i in range(0, len(data), page_size)]
    pagination = {'current_page': page, 'page_size': page_size, 'total_items': len(data)}

    if page > len(paginated_data):
        return [], pagination

    return paginated_data[page - 1], pagination


def is_list(value: str):
    try:
        list_str = eval(value)
        return isinstance(list_str, list)
    except:
        return False


def is_valid_email(email: str) -> bool:
    pattern = re.compile("^\w+(\.\w+)*@.+\.[a-zA-Z]{2,}$")
    return bool(re.match(pattern, email))


def parse_accept_language(accept_languages: str) -> str:
    if accept_languages:
        languages = accept_languages.split(",")
        for language in languages:
            lang = language.split(";")[0].strip()
            if lang[:2] in ["vi", "en"]:
                return lang[:2]
    return "vi"


def is_same_dict(dict1: dict, dict2: dict) -> bool:
    if sorted(list(dict1.keys())) != sorted(list(dict2.keys())):
        return False

    for (key1, value1), (key2, value2) in zip(sorted(dict1.items(), key=lambda k: k[0]),
                                              sorted(dict2.items(), key=lambda k: k[0])):
        if isinstance(value1, dict) and isinstance(value2, dict):
            return is_same_dict(value1, value2)
        elif isinstance(value1, dict) or isinstance(value2, dict):
            return False
        else:
            if isinstance(value1, list) and isinstance(value2, list):
                if len(value1) != len(value2):
                    return False

                if len(value1) >= 1 and isinstance(value1[0], dict) and isinstance(value2[0], dict):
                    for element_in_value1, element_in_value2 in zip(value1, value2):
                        if not is_same_dict(element_in_value1, element_in_value2):
                            return False
                elif sorted(value1) != sorted(value2):
                    return False
            elif value1 != value2:
                return False

    return True


def generate_unique_filename(filename: str):
    return filename.split('.')[0] + '-' + str(round(time.time() * 1000)) + '.' + filename.split('.')[1]