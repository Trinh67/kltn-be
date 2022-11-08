import pytest


def test_get_list_file(session, client):
    """
        name: Test get list file
    """
    session.commit()

    resp = client.get('/api/v1/category/list-category')

    assert resp.status_code == 200
    assert resp.json().get('code') == 200
    assert len(resp.json().get('data').get('categories')) == 2