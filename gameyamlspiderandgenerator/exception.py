class InitializeFailed(Exception):
    def __init__(self):
        super().__init__("Failed to initialize")


class ReadOrWriteConfigFailed(Exception):
    def __init__(self):
        super().__init__("Failed to read or write config")


class CommunicateWithServerFailed(Exception):
    def __init__(self, status_code: int = None):
        self.status_code = status_code
        super().__init__(
            f"Failed to communicate with server, status code: {status_code}"
        )


class ResponseNotInitialized(Exception):
    def __init__(self, url: str):
        super().__init__(f"Response not initialized, url: {url}")


class InvalidResponse(Exception):
    def __init__(self, url: str):
        super().__init__(f"Invalid response, url: {url}")
