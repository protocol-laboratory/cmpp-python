import threading


class BoundAtomic:
    def __init__(self, min_val: int, max_val: int):
        assert min_val <= max_val, "min must be less than or equal to max"
        self.min = min_val
        self.max = max_val
        self.value = min_val
        self.lock = threading.Lock()

    def next_val(self) -> int:
        with self.lock:
            if self.value >= self.max:
                self.value = self.min
            else:
                self.value += 1
            return self.value
