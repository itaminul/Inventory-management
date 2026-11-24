import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger("inventory.api")


async def request_logging_middleware(
    request: Request,
    call_next
):

    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    try:
        response = await call_next(request)

        process_time = time.perf_counter() - start_time

        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request ID=%s Method=%s Path=%s Status=%s Duration=%.4fs",
            request_id,
            request.method,
            request.url.path,
            response.status_code,
            process_time
        )

        return response

    except Exception:
        logger.exception(
            "Request ID=%s Method=%s Path=%s failed",
            request_id,
            request.method,
            request.url.path
        )
        raise