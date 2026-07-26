from collections.abc import Callable


class StreamHandlerContext:
    """封装统一流式消息输出"""

    def __init__(self, stream_handler: Callable[[str], None]):
        self._stream_handler = stream_handler

    def emit(self, message: str):
        """透传 SSE 消息"""
        self._stream_handler(message)
