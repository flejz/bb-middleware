
from enum import Enum

class StorageType(Enum):
    KEY_VALUE = 0
    LIST = 1

class StorageFactory:
    def __init__(self, storage):
        self.storage = storage

    def branch(self, ref, storage_type):
        return self.storage(ref, storage_type)
