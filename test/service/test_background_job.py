import pytest
from setting import setting
from unittest.mock import Mock, patch
from app.model.file import File
from app.service.background_job import BackgroundJobService

from test.faker.file import FileProvider


@patch('app.adapter.elastic.ElasticService.call')
def test_get_list_file(mock_elastic, session):
    """
        name: Test get list file
    """
    mock_elastic.return_value = Mock(status_code=201,
                                         json=lambda: {
                                                        "_id": "750248261205495808"
                                                    })
    FileProvider.create_file_model(session, id=3, status=0)
    session.commit()

    BackgroundJobService.upload_file_to_elastic_search(session)

    files = File.q(session, File.status == 0).all()
    assert len(files) == 0