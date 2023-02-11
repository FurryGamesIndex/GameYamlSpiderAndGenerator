from textwrap import dedent
from typing import AnyStr

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString


def pss_dedent(x: AnyStr) -> PreservedScalarString:
    return PreservedScalarString(dedent(x))


fgi = YAML(typ=["rt", "string"])
fgi.indent(sequence=4, offset=2)
fgi.preserve_quotes = True
fgi.width = 4096


def dump_to_yaml(data: dict) -> AnyStr:
    temp = fgi.dump_to_string(data)
    for i in list(data.keys())[1:]:
        temp = temp.replace("\n" + i, "\n\n" + i)
    return temp
