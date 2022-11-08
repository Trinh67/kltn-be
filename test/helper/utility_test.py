import pytest

from app.util.common import is_phone_number_valid, is_valid_email, parse_accept_language


@pytest.mark.parametrize(
    'phone_number, expected',
    [
        ('84564854786', True),
        ('0564854786', True),
        ('564854786', True),
        ('0988169532', True),
        ('055555', False),
        ('098888888888888', False),
        ('055555vv', False),
        ('0988888888hhhhhh', False),
        ('kkkkkkkkvv', False),
        ('kkkkkkkkkkkhhhhhh', False)
    ]
)
def test_is_phone_number_valid(phone_number: str, expected: bool):
    assert is_phone_number_valid(phone_number=phone_number) == expected


@pytest.mark.parametrize(
    "email, expected_is_valid",
    [
        ("abCdEf@gmail.com", True),
        ("abcdef@gmail.com", True),
        ("abc.def@gmail.com", True),
        ("abc.def@gmail.vn", True),
        ("á.abcdef@gmail.com", True),
        ("abc$def@gmail.vn", False),
        ("abc^def@gmail.vn", False),
        ("abc..def@gmail.vn", False),
        ("a!#$%&'*+-/=?^_`{|}~@gmail.com", False),
        (".abcdef@gmail.com", False),
        ("ab<>ef@gmail.com", False),
    ]
)
def test_email_validation(email, expected_is_valid):
    assert expected_is_valid == is_valid_email(email)


@pytest.mark.parametrize(
    "accept_languages,expected",
    [
        ("vi-VN,en;q=0.7", "vi"),
        ("vi;q=0.7", "vi"),
        ("en;q=0.7", "en"),
        ("vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7", "vi"),
        ("en-US;q=0.8,en;q=0.7,vi-VN,vi;q=0.9", "en"),
        ("vi;q=0.9,en-US;q=0.8,en;q=0.7,vi-VN", "vi"),
        ("fr-FR;q=0.6,fr;q=0.5,en;q=0.7,vi-VN", "en"),
        ("fr-FR;q=0.6,fr;q=0.5", "vi"),
        ('application/json', "vi")
    ]
)
def test_parse_accept_language(accept_languages: str, expected: str):
    assert parse_accept_language(accept_languages) == expected