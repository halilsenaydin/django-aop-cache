"""
Result Classes for API Responses

This module defines a hierarchy of result classes used to standardize the structure of API responses.
These classes encapsulate the outcome of operations, including success and error scenarios.

Classes:
1. Result:
   - A base class that represents the outcome of an operation, indicating whether it was successful
     and providing a message.

2. SuccessResult:
   - Inherits from Result.
   - Represents a successful operation with a success flag set to True.

3. ErrorResult:
   - Inherits from Result.
   - Represents a failed operation with a success flag set to False.

4. DataResult(Generic[T]):
   - A generic subclass of Result that includes additional data alongside the success status and message.
   - This allows for responses that carry data relevant to the operation.

5. SuccessDataResult(DataResult[T]):
   - Inherits from DataResult.
   - Represents a successful operation that returns data, with the success flag set to True.

6. ErrorDataResult(DataResult[T]):
   - Inherits from DataResult.
   - Represents a failed operation that returns data, with the success flag set to False.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class Result:
    def __init__(self, success: bool, message: str):
        self.success = success
        self.message = message


class SuccessResult(Result):
    def __init__(self, message):
        super().__init__(True, message)


class ErrorResult(Result):
    def __init__(self, message):
        super().__init__(success=False, message=message)


class DataResult(Generic[T], Result):
    def __init__(self, success: bool, message: str, data: T):
        super().__init__(success, message)
        self.data = data


class SuccessDataResult(DataResult[T]):
    def __init__(self, data: T, message: str):
        super().__init__(True, message, data)


class ErrorDataResult(DataResult[T]):
    def __init__(self, data: T, message: str):
        super().__init__(False, message, data)
