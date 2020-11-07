#!/usr/bin/env python3
import json
import glob
import sys

result = {}

for filename in sorted(glob.glob("result*.json")):
    with open(filename) as f:
        j = json.load(f)
    result[filename] = [
        key for key, value in j["candidates"].items() if value["valid"]
    ]

json.dump(result, sys.stdout, indent=2)
