explain = {'0': 'Task executed successfully.',
           '-1': 'Error during initialization.',
           '-2': 'Error reading or writing configuration file',
           '-3': 'An error occurred while communicating with the server.'}
from typing import SupportsInt
import http.client


def get_code_explain(code: SupportsInt):
    return explain[str(code)] if str(code) in explain else http.client.responses[code]
