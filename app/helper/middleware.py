from typing import Optional

from fastapi import Request
from humps import camelize


async def get_action_by_from_request(request: Request) -> Optional[str]:
    if request.method in ['POST', 'PUT', 'PATCH']:
        request_body = await request.json()
        user = request_body.get(camelize('action_by'))
        if not user:
            user = request_body.get(camelize('created_by'))

        return user
    elif request.method == 'DELETE':
        user = request.query_params.get(camelize('deleted_by'))
        # if not user:
        #     request_body = await request.json()
        #     user = request_body.get(camelize('action_by'))

        return user
    return None