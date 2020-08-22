from storage.generic import GenericStorage

class MemoryStorage(GenericStorage):
    def __init__(self, ref, storage_type):
        GenericStorage.__init__(self, ref, storage_type)

    def persist(self, key = None):
        if self.hashmap.get(self.ref) is None:
            self.hashmap[self.ref] = {}
        if key != None and self.hashmap[self.ref].get(key) is None:
            self.hashmap[self.ref][key] = None

    def update(self, key, data):
        self.persist(key)
        self.hashmap[self.ref][key] = data
        return self.hashmap[self.ref][key]

    def get(self, key):
        self.persist(key)
        return self.hashmap[self.ref][key]

    def get_all(self):
        if self.is_list():
            return self.list
        else:
            self.persist()
            return self.hashmap[self.ref]

