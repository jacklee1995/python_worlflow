from enum import Enum
from typing import List

class OutputErrorType(Enum):
    NETWORK_ERROR = "network_error"
    FILE_SYSTEM_ERROR = "file_system_error"
    BUFFER_OVERFLOW = "buffer_overflow"
    INVALID_DATA = "invalid_data"
    PERMISSION_ERROR = "permission_error"
    CONNECTION_ERROR = "connection_error"
    TIMEOUT_ERROR = "timeout_error"


class RetryPolicy:
    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.1,
                 max_delay: float = 30.0, retry_on: List[OutputErrorType] = None):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.retry_on = retry_on or []


class OutputMetrics:
    def __init__(self):
        self.bytes_written = 0
        self.write_count = 0
        self.error_count = 0
        self.retry_count = 0
        self.write_speed = 0.0
        self.last_write_time = 0.0