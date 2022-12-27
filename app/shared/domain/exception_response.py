import traceback

from fastapi.responses import JSONResponse


class ExceptionResponse(JSONResponse):
    def __init__(self, exception: Exception, status_code: int = 400, return_traceback: bool = False):
        content = {
            "detail": str(exception)
        }
        if return_traceback:
            content["traceback"] = traceback.format_exc()
        super().__init__(content, status_code, None, None, None)
