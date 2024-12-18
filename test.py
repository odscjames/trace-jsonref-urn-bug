import os
import jsonref
import pathlib
import referencing
import json

base_uri = pathlib.Path(
    os.path.dirname(__file__) + "/"
).as_uri() + "/"

with open("libs.json") as fp:
    resource = referencing.Resource.from_contents(json.load(fp))

registry = resource @ referencing.Registry()


def _jsonref_loader(uri):
    global registry
    print("LOADING {}".format(uri))
    if uri.startswith("urn:"):
        if uri in registry:
            return registry.contents(uri)
        else:
            raise Exception("URN {} not found".format(uri))
    return jsonref.jsonloader(uri)


with open("start.json") as fp:
    start = json.load(fp)

print("TEST 1 - WORKS GREAT!")
print(jsonref.JsonRef.replace_refs(start, base_uri=base_uri, loader=_jsonref_loader))

print("TEST 2 - FAILS!")
start["properties"]["home_address"]["$ref"] = "urn:library#/$defs/address"
print(jsonref.JsonRef.replace_refs(start, base_uri=base_uri, loader=_jsonref_loader))
