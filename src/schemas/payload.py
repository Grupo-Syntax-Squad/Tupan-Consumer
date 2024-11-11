class SchemaPayload:
    def __init__(self, mac: str, data: dict, timestamp: float):
        self.mac = mac
        self.data = data
        self.timestamp = timestamp
