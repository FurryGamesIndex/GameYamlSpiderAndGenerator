from textwrap import dedent
from typing import AnyStr

from ruamel.yaml import YAML
from ruamel.yaml.scalarstring import PreservedScalarString


def pss_dedent(x: AnyStr) -> PreservedScalarString:
    return PreservedScalarString(dedent(x))


yaml = YAML(typ=["rt", "string"])
yaml.indent(sequence=4, offset=2)
yaml.width = 4096


def dump_to_yaml(data: dict) -> AnyStr:
    temp = yaml.dump_to_string(data)
    for i in list(data.keys())[1:]:
        b_ret = temp.replace("\n" + i, "\n\n" + i)
    return temp
