#!/usr/bin/env python3
import json
import glob
import sys

HEADER = (
    "Name",
    "can verify",
    "loaded CA certs",
    "CA file",
    # "file certs",
    "CA path",
    "path certs",
    # "OpenSSL version",
)


def analyze():
    result = [HEADER]
    result.append(tuple("---" for _ in HEADER))

    for filename in sorted(glob.glob("result*.json")):
        with open(filename) as f:
            j = json.load(f)

        entry = (
            j["name"],
            ":heavy_check_mark:" if j["can_connect"]["verified"] else ":x:",
            j["default_context"]["ca_certs_count"],
            j["default_verify"]["cafile"]["path"],
            # j["default_verify"]["cafile"]["certs"],
            j["default_verify"]["capath"]["path"],
            j["default_verify"]["capath"]["certs"],
            # j["openssl"]["version"],
        )

        result.append(entry)

    for entry in result:
        print(" | ".join(str(e) if e is not None else "" for e in entry))


if __name__ == "__main__":
    analyze()
