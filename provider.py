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

    def persist(self, ref, ref_id = None):
        if self.store.get(ref) is None:
            self.store[ref] = {}
        if ref_id != None and self.store[ref].get(ref_id) is None:
            self.store[ref][ref_id] = None

    def update(self, ref, ref_id, data):
        self.persist(ref, ref_id)
        self.store[ref][ref_id] = data
        return self.store[ref][ref_id]

    def get_all(self, ref):
        self.persist(ref)
        return self.store[ref]

    def get(self, ref, ref_id):
        self.persist(ref, ref_id)
        return self.store[ref][ref_id]
