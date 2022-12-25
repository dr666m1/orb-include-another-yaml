import contextlib
import os
import yaml

import jsonpath_ng


class Error(Exception):
    """Base-class for all exceptions raised by this module"""


class Import(yaml.YAMLObject):
    yaml_tag = "!include"

    @classmethod
    def from_yaml(cls, _, node):
        filepath = None
        jsonpath = "$"

        if isinstance(node, yaml.ScalarNode):
            filepath = node.value
        elif isinstance(node, yaml.MappingNode):
            for item in node.value:
                match key := item[0].value:
                    case "filepath":
                        filepath = item[1].value
                    case "jsonpath":
                        jsonpath = item[1].value
                    case _:
                        raise Error(f"got unexpected parameter: {key}")
        else:
            raise Error(
                f"expected ScalarNode or MappingNode but got: {node.__class__.__name__}"
            )

        if filepath is None:
            raise Error("filepath is not specified!")

        filepath = os.path.abspath(filepath)
        with (
            open(filepath, "r") as f,
            contextlib.chdir(os.path.dirname(filepath)),
        ):
            obj = yaml.full_load(f)

        temp = jsonpath_ng.parse(jsonpath).find(obj)
        if len(temp) == 1:
            obj = temp[0].value
        else:
            obj = [x.value for x in temp]

        return obj


def main(filepath=None, overwrite=True):
    if filepath is None:
        filepath = os.getenv("PARAM_FILEPATH")

    if filepath is None:
        raise Error("PARAM_FILEPATH is not specified!")

    filepath = os.path.abspath(filepath)
    with (
        open(filepath, "r") as f,
        contextlib.chdir(os.path.dirname(filepath)),
    ):
        obj = yaml.full_load(f)

    if overwrite:
        with open(filepath, "w") as f:
            f.write(yaml.dump(obj))

    return obj


if __name__ == "__main__":
    main()
