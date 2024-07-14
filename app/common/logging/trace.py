import threading
from uuid import uuid4


class ThreadLocalContextManager:
    thread_local = threading.local()

    def set_trace(self):
        self.thread_local.django_trace = uuid4().hex[:16]

    def get_trace(self) -> str:
        return getattr(self.thread_local, "django_trace", None)


thread_local_ctx = ThreadLocalContextManager()
