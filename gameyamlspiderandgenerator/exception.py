class InitializeFailed(Exception):
    def __init__(self):
        super().__init__("Failed to initialize")


class ReadOrWriteConfigFailed(Exception):
    def __init__(self):
        super().__init__("Failed to read or write config")


class CommunicateWithServerFailed(Exception):
    def __init__(self, info: int | str = ""):
        super().__init__(
            f"Failed to communicate with server, {('status code: ' + str(info)) if isinstance(info, int) else info}"
        )


class ResponseNotInitialized(Exception):
    def __init__(self, url: str):
        super().__init__(f"Response not initialized, url: {url}")


class InvalidResponse(Exception):
    def __init__(self, url: str):
        super().__init__(f"Invalid response, url: {url}")
