from http import HTTPStatus


class GenerateError(Exception):
    pass


class HookError(GenerateError):
    pass


class ApiKeyNotFoundError(HookError):
    def __init__(self, hook: str):
        super().__init__(f"The {hook} hook API key is required but not configured.")


class PluginNotLoadedError(GenerateError):
    def __init__(self):
        super().__init__("Did you forget to use config.load()?")


class InvalidUrlError(GenerateError, ValueError):
    pass


class ReadOrWriteConfigFailed(GenerateError, IOError):
    pass


class InvalidTargetResourceError(GenerateError, ConnectionError):
    def __init__(self, code: int):
        super().__init__(f"{code}: {HTTPStatus(code).description}")


class ResponseNotInitialized(GenerateError):
    def __init__(self, url: str):
        super().__init__(f"Response not initialized, url: {url}")


class InvalidResponse(GenerateError):
    def __init__(self, url: str):
        super().__init__(f"Invalid response, url: {url}")
