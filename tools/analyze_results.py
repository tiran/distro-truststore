#!/usr/bin/env python3
import json
import glob
import sys

result = {}

for filename in sorted(glob.glob("result*.json")):
    name = filename[len("result-") :].rsplit(".", 1)[0]

    with open(filename) as f:
        j = json.load(f)

    openssldirs = [
        key for key, value in j["candidates_openssldir"].items() if value["valid"]
    ]
    if j["default_verify"]["truststore"]:
        dvp = dict(
            cafile=j["default_verify"]["cafile"]["path"],
            cafile_valid=bool(j["default_verify"]["cafile"]["certs"]),
            capath=j["default_verify"]["capath"]["path"],
            capath_valid=bool(j["default_verify"]["capath"]["certs"]),
        )
    else:
        dvp = None

    ca_certs_count = j["default_context"]["ca_certs_count"]
    can_connect = j["can_connect"]["verified"]

    result[name] = dict(
        name=j["name"],
        openssldirs=openssldirs,
        default_verify_paths=dvp,
        default_context_can_verify=can_connect,
        default_context_ca_certs_count=ca_certs_count,
        openssl_version=j["openssl"]["version"],
    )

json.dump(result, sys.stdout, indent=2, sort_keys=True)
