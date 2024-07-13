import logging
import re

from django.http.request import HttpRequest
from rest_framework.response import Response

from app.common.logging.trace import thread_local_ctx

logger = logging.getLogger("app.request")


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> Response:
        path = f"{request.method} {request.get_full_path()}"
        self._logging_request(path, request)
        response = self.get_response(request)
        self._logging_response(path, response)
        return response

    def _logging_request(self, path: str, request: HttpRequest):
        thread_local_ctx.set_trace()
        logger.info(path)
        if (
            (request_body := request.body)
            and re.search(r"^application/json", request.content_type)
        ):
            logger.info(f"Request - {request_body.decode()}")

    def _logging_response(self, path: str, response: Response):
        logger.info(f"{path} - {response.status_code}")
        if re.search(r"^application/json", response.get("Content-Type", "")):
            logger.info(f"Response - {response.data}")
