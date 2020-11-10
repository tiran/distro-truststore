#!/usr/bin/env python3
import json
import glob
import sys

result = {}

for filename in sorted(glob.glob("result*.json")):
    with open(filename) as f:
        j = json.load(f)

    name = j["name"]
    openssldirs = [
        key
        for key, value in j["candidates_openssldir"].items()
        if value["valid"]
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

    result[name] = dict(
        openssldirs=openssldirs,
        default_verify_paths=dvp,
        default_context_can_verify=bool(ca_certs_count),
        default_context_ca_certs_count=ca_certs_count,
        openssl_version=j["openssl"]["version"]
    )

json.dump(result, sys.stdout, indent=2, sort_keys=True)
