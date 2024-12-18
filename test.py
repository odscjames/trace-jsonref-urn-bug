import os
import jsonref
import pathlib
import json

base_uri = pathlib.Path(
    os.path.dirname(__file__) + "/"
).as_uri() + "/"

with open("libs.json") as fp:
    lib = json.load(fp)

def _jsonref_loader(uri):
    global lib
    print("LOADING {}".format(uri))
    if uri == "urn:library":
        return lib
    return jsonref.jsonloader(uri)


with open("start.json") as fp:
    start = json.load(fp)

print("TEST 1 - WORKS GREAT!")
print(jsonref.JsonRef.replace_refs(start, base_uri=base_uri, loader=_jsonref_loader))

print("TEST 2 - FAILS!")
start["properties"]["home_address"]["$ref"] = "urn:library#/$defs/address"
print(jsonref.JsonRef.replace_refs(start, base_uri=base_uri, loader=_jsonref_loader))
