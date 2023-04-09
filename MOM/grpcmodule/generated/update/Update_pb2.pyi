from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LogResponse(_message.Message):
    __slots__ = ["data", "is_successful"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    is_successful: bool
    def __init__(self, is_successful: bool = ..., data: _Optional[bytes] = ...) -> None: ...

class Request(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateResponse(_message.Message):
    __slots__ = ["is_successful", "log_data", "queue_data", "topic_data", "users_data"]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    LOG_DATA_FIELD_NUMBER: _ClassVar[int]
    QUEUE_DATA_FIELD_NUMBER: _ClassVar[int]
    TOPIC_DATA_FIELD_NUMBER: _ClassVar[int]
    USERS_DATA_FIELD_NUMBER: _ClassVar[int]
    is_successful: bool
    log_data: bytes
    queue_data: bytes
    topic_data: bytes
    users_data: bytes
    def __init__(self, is_successful: bool = ..., queue_data: _Optional[bytes] = ..., users_data: _Optional[bytes] = ..., topic_data: _Optional[bytes] = ..., log_data: _Optional[bytes] = ...) -> None: ...
