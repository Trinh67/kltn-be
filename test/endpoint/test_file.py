import pytest
from app.dto.core.auth import UserDTO
from app.dto.core.file import UpdateStatusFileRequest
from app.helper.enum import FileStatus
from app.model.file import File
from app.service.file import FileService

from test.faker.file import FileProvider
from test.faker.user import UserProvider


mock_admin = {
    "name": "Trinh Xuan Trinh",
    "email": "trinhxuantrinh.yd267@gmail.com",
    "user_id": "123456789"
}

mock_user = {
    "name": "Trinh Xuan Trinh",
    "email": "trinh.yd267@gmail.com",
    "user_id": "123456789"
}

@pytest.mark.parametrize(
    "query, expected_http_code, expected_code",
    [
        ("?id=3", 200, 200),
        ("?id=9999999999", 400, 404)
    ]
)
def test_get_file(session, client, query, expected_http_code, expected_code):
    """
        name: Test get file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=3)

    session.commit()

    resp = client.get('/api/v1/file/' + query)

    assert resp.status_code == expected_http_code
    assert resp.json().get('code') == expected_code


def test_get_list_file(session, client):
    """
        name: Test get list file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=3, status=3)
    FileProvider.create_file_model(session, id=4, status=3)

    session.commit()

    resp = client.get('/api/v1/file/list-file')

    assert resp.status_code == 200
    assert resp.json().get('code') == 200
    assert len(resp.json().get('data').get('files')) == 2

@pytest.mark.parametrize(
    "type, expected_num",
    [
        (FileStatus.PROCESSING, 0),
        (FileStatus.DRAFT, 0),
        (FileStatus.REFUSE, 1),
        (FileStatus.APPROVED, 2)
    ]
)
def test_admin_filter_file(session, type, expected_num):
    """
        name: Test filter file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=2, status=3)
    FileProvider.create_file_model(session, id=3, status=3)
    FileProvider.create_file_model(session, id=4, status=2)

    session.commit()

    resp, pagination = FileService.filter_file(session, type = type, user = UserDTO.parse_obj(mock_admin))

    assert len(resp.files) == expected_num


@pytest.mark.parametrize(
    "type, expected_num",
    [
        (FileStatus.UPLOADED, 3),
        (FileStatus.LIKED, 0),
        (FileStatus.SHARED, 0)
    ]
)
def test_user_filter_file(session, type, expected_num):
    """
        name: Test filter file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=2, status=3)
    FileProvider.create_file_model(session, id=3, status=3)
    FileProvider.create_file_model(session, id=4, status=2)

    session.commit()

    resp, pagination = FileService.filter_file(session, type = type, user = UserDTO.parse_obj(mock_user))

    assert len(resp.files) == expected_num


def test_approved_file(session):
    """
        name: Test approved file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=2, status=1)

    session.commit()

    resp = FileService.update_status_file(session, \
                                        request = UpdateStatusFileRequest.parse_obj({"id": 2, "type": 3, "google_driver_id": 123}), \
                                        user = UserDTO.parse_obj(mock_admin))

    files = File.q(session, File.status == 3).all()
    assert len(files) == 1


def test_refuse_file(session):
    """
        name: Test refuse file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=2, status=1)

    session.commit()

    resp = FileService.update_status_file(session, \
                                        request = UpdateStatusFileRequest.parse_obj({"id": 2, "type": 2, "refuse_reason": "tep bi loi"}), \
                                        user = UserDTO.parse_obj(mock_admin))

    files = File.q(session, File.status == 2).all()
    assert len(files) == 1


def test_get_statistic_file(session):
    """
        name: Test get statistic file
    """
    UserProvider.create_user_model(session, id=1)
    FileProvider.create_file_model(session, id=2, status=0)
    FileProvider.create_file_model(session, id=3, status=1)
    FileProvider.create_file_model(session, id=4, status=2)
    FileProvider.create_file_model(session, id=5, status=3)

    session.commit()

    resp = FileService.get_statistic_file(session, user = UserDTO.parse_obj(mock_user))

    assert len(resp.files) == 6