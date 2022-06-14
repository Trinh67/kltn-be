from typing import Sequence
from app.dto.base import OpenApiResponseModel


def map_resp_to_openapi(list_res: Sequence[OpenApiResponseModel]):
    responses = {}
    # Format response to open api response
    for res in list_res:

        # Add space with http similar together
        while res.http_code in responses:
            res.http_code += " "

        # Add data with res has data
        if res.data:
            responses[res.http_code] = {
                "description": res.description,
                "content": {
                    "application/json": {
                        "example": {
                            "code": res.code,
                            "message": res.message,
                            "data": res.data
                        }
                    }
                }
            }
        else:
            responses[res.http_code] = {
                "description": res.description,
                "content": {
                    "application/json": {
                        "example": {
                            "code": res.code,
                            "message": res.message
                        }
                    }
                }
            }

    # Add space to 500 errors to make it in bottom
    if responses.get("500"):
        responses["500" + " " * (len(max(responses.keys(), key=len)) - 3)] = responses.pop("500")
    return responses