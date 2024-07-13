from logging import Filter, LogRecord

from .trace import thread_local_ctx


class TraceFilter(Filter):
    def filter(self, record: LogRecord) -> bool:
        record.trace = thread_local_ctx.get_trace()
        return True
