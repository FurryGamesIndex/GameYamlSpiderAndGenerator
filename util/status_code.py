explain = {'0': 'Task executed successfully.',
            '-1': 'Error during initialization.',
            '-2': 'Error reading or writing configuration file',
           '-3': 'An error occurred while communicating with the server.'}
from typing import SupportsInt

def get_code_explain(code: SupportsInt):
    return explain[str(code)]
