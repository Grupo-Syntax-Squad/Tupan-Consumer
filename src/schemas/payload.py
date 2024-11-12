class SchemaPayload:
    def __init__(self, mac: str, data: dict, timestamp: float):
        self.mac: str = mac
        self.data: dict = data
        self.timestamp: float = timestamp
