import re
import time


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


def paginate(data, page, page_size):
    paginated_data = [data[i: i + page_size] for i in range(0, len(data), page_size)]
    pagination = {'current_page': page, 'page_size': page_size, 'total_items': len(data)}

    if page > len(paginated_data):
        return [], pagination

    return paginated_data[page - 1], pagination


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


def generate_unique_filename(filename: str):
    return filename.split('.')[0] + '-' + str(round(time.time() * 1000)) + '.' + filename.split('.')[-1]