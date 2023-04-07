from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Json(_message.Message):
    __slots__ = ["data", "filename"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    filename: str
    def __init__(self, filename: _Optional[str] = ..., data: _Optional[bytes] = ...) -> None: ...

class ReplicateResponse(_message.Message):
    __slots__ = ["is_successful", "message"]
    IS_SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    is_successful: bool
    message: str
    def __init__(self, is_successful: bool = ..., message: _Optional[str] = ...) -> None: ...
