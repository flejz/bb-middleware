class GenericStore:
    def __init__(self, provider, ref):
        self.provider = provider
        self.ref = ref

    def update(self, ref_id, data):
        return self.provider.update(self.ref, ref_id, data)

    def get_all(self):
        return self.provider.get_all(self.ref)

    def get(self, ref_id):
        return self.provider.get(self.ref, ref_id)
