

class DBConnectionError(Exception):
    """Raised when a repository could not stablish a connection"""

    def __init__(self, db_type: str):
        self.message = f"Connection to '{db_type}' has failed, please check your DB"
        super().__init__(self.message)

class UrlWithMoreParamsAsExpected(Exception):
    """Raised when an URL has more parameters as excepted"""

    def __init__(self, expected_num_of_params: int, actual_num_of_params: int):
        super().__init__(f"URL has {actual_num_of_params} (expected={expected_num_of_params})")
