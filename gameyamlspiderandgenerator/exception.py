class GenerateError(Exception):
    pass


class PluginNotLoadedError(GenerateError):
    pass


class InvalidUrlError(GenerateError):
    pass


class ReadOrWriteConfigFailed(GenerateError):
    def __init__(self):
        super().__init__("Failed to read or write config")


class InvalidTargetResourceError(GenerateError):
    def __init__(self, code: int):
        super().__init__(f"The target resource is no longer valid.status code: {code}")


class ResponseNotInitialized(GenerateError):
    def __init__(self, url: str):
        super().__init__(f"Response not initialized, url: {url}")


class InvalidResponse(GenerateError):
    def __init__(self, url: str):
        super().__init__(f"Invalid response, url: {url}")
