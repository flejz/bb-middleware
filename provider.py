class GenericProvider:
    def update(self, ref, ref_id, data):
        pass

    def get(self, ref, ref_id):
        pass

    def get_all(self, ref):
        pass

class MemoryProvider(GenericProvider):
    def __init__(self):
        self.store = {}

    def update(self, ref, ref_id, data):
        if self.store.get(ref) is None:
            self.store[ref] = {}
        self.store[ref][ref_id] = data

    def get_all(self, ref):
        return self.store[ref]
