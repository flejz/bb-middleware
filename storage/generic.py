from storage.factory import StorageType

class GenericStorage:
    def __init__(self, ref, storage_type):
        self.ref = ref
        self.storage_type = storage_type
        self.hashmap = {}
        self.list = []

    def update(self, key, data):
        pass

    def get(self, key):
        pass

    def get_all(self):
        pass

    def add(self, data):
        self.list.append(data)

    def is_list(self):
        return self.storage_type == StorageType.LIST
