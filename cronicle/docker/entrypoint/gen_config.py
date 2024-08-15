#!/usr/bin/env python
import os
from glob import glob
import json

from numpy import spacing


prefix_name_plugin = "global/plugins"
first_line = {"page_size": 50, "first_page": 0, "last_page": 0, "length": 0, "type": "list"}
second_line = {"type": "list_page", "items": []}


def json_dumps(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def gen_plugin(plugins):
    first_line["length"] = len(plugins)
    second_line["items"] = plugins
    print(f"{prefix_name_plugin} -", json_dumps(first_line))
    print(f"{prefix_name_plugin}/0 -", json_dumps(second_line))

    # print(json.dumps(config))


def read_plugin():
    files = glob("config/*-plugin.json")
    if len(files) == 0:
        raise Exception("No plugin files found")
    plugins = []
    files.sort()
    for file in files:
        data = json.load(open(file))
        if not isinstance(data, list):
            raise Exception(f"Invalid plugin file: {file}")
        plugins.extend(data)
    return plugins


if __name__ == "__main__":
    gen_plugin(read_plugin())
