class InitializeFailed(Exception):
    def __init__(self):
        super().__init__("Failed to initialize")


class ReadOrWriteConfigFailed(Exception):
    def __init__(self):
        super().__init__("Failed to read or write config")


class InvalidTargetResourceError(Exception):
    def __init__(self, code: int):
        super().__init__(f"The target resource is no longer valid.status code: {code}")


class ResponseNotInitialized(Exception):
    def __init__(self, url: str):
        super().__init__(f"Response not initialized, url: {url}")


class InvalidResponse(Exception):
    def __init__(self, url: str):
        super().__init__(f"Invalid response, url: {url}")