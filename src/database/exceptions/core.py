from typing import Optional, Any


exceptions_holder = {}


class BaseDbException(Exception):
    def __init__(self, config: Optional[Any]):
        self.config = config
        global exceptions_holder
        exceptions_holder[self.config.id] = {k: v for k, v in config.__dict__.items() if '__' not in k}
        exceptions_holder = dict(sorted(exceptions_holder.items()))
        with open('/database/../exceptions.json', 'w') as f:
            f.write(str(exceptions_holder))

    def generate_http_exception(self) -> (int, str):
        return self.config.status_code, self.config.description

    def get_exception_id(self) -> int:
        return self.config.id
