import contextlib
import os
import yaml


class Import(yaml.YAMLObject):
    yaml_tag = "!include"

    @classmethod
    def from_yaml(cls, _, node):
        filepath = None
        keypath = None

        if isinstance(node, yaml.ScalarNode):
            filepath = node.value
        else:
            for item in node.value:
                match key := item[0].value:
                    case "filepath":
                        filepath = item[1].value
                    case "keypath":
                        keypath = item[1].value
                    case _:
                        raise Exception(f"got unnexpected parameter: {key}")

        if filepath is None:
            raise Exception("filepath is not specified!")

        with open(filepath, "r") as f:
            obj = yaml.full_load(f)

        if keypath is not None:
            obj = obj[keypath]
        return obj


def main(filepath=None, overwrite=True):
    if filepath == None:
        filepath = os.getenv("PARAM_FILEPATH")

    if filepath is None:
        raise Exception("PARAM_FILEPATH is not specified!")

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
