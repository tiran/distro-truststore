#!/usr/bin/env python3
import os
import json
import re
import ssl
import sys


# hash symlink name, e.g. 2e5ac55d.0
_hashfile_re = re.compile(r"^[a-f\d]{8}\.\d$")
# standard or trusted PEM certificate
_pem_re = re.compile(
    (
        "^-----BEGIN (?P<trusted>(TRUSTED )?)CERTIFICATE-----\n"
        "(?P<base64>[a-zA-Z0-9+/\n]+?[=]{0,2})\n"
        "^-----END (?P=trusted)?CERTIFICATE-----"
    ),
    re.MULTILINE,
)
# freedesktop.org os-release file
_osrelease_line = re.compile(
    "^(?!#)(?P<name>[a-zA-Z0-9_]+)="
    "(?P<quote>[\"']?)(?P<value>.+)(?P=quote)$"
)


def path_info(path):
    if path and os.path.isfile(path):
        with open(path) as f:
            certs = _pem_re.findall(f.read())
        return dict(
            path=path,
            exists=True,
            type="file",
            size=os.path.getsize(path),
            certs=len(certs),
        )
    if path and os.path.isdir(path):
        files = os.listdir(path)
        certs = [f for f in files if _hashfile_re.match(f)]
        return dict(
            path=path,
            exists=True,
            type="dir",
            size=len(files),
            certs=len(certs),
        )
    return dict(path=path, exists=False, type=None, size=0, certs=0,)


def read_os_release(filenames=("/etc/os-release", "/usr/lib/os-release")):
    """Parser for /etc/os-release for Linux distributions

    https://www.freedesktop.org/software/systemd/man/os-release.html

    /etc/os-release is the primary location of os-release file. The fallback
    /usr/lib/os-release is used by ArchLinux.
    """
    # default values according to standard
    release = {
        "NAME": "Linux",
        "ID": "linux",
    }
    for filename in filenames:
        try:
            with open(filename) as f:
                for line in f:
                    mo = _osrelease_line.match(line)
                    if mo is not None:
                        release[mo.group("name")] = mo.group("value")
        except FileNotFoundError:
            pass

    # parse ID_LIKE as tuple
    if "ID_LIKE" in release:
        release["ID_LIKE"] = tuple(
            v.strip() for v in release["ID_LIKE"].split(" ") if v.strip()
        )
    else:
        # always provide ID_LIKE
        release["ID_LIKE"] = ()
    return release


def check_candidates(candidates=("/etc/ssl", "/etc/pki/tls")):
    result = {}
    for candidate in candidates:
        if not os.path.isdir(candidate):
            result[candidate] = dict(valid=False)
        else:
            cafile = path_info(os.path.join(candidate, "cert.pem"))
            capath = path_info(os.path.join(candidate, "certs"))
            openssl_conf = path_info(os.path.join(candidate, "openssl.cnf"))
            valid = bool(cafile["certs"] or capath["certs"])
            result[candidate] = dict(
                cafile=cafile,
                capath=capath,
                openssl_conf=openssl_conf,
                valid=valid,
            )
    return result


def get_info():
    vp = ssl.get_default_verify_paths()
    openssl_cnf = os.path.join(os.path.dirname(vp.cafile), "openssl.cnf")
    cafile = path_info(vp.cafile)
    capath = path_info(vp.capath)

    return dict(
        os_release=read_os_release(),
        sys_platform=sys.platform,
        os_name=os.name,
        default_verify_paths=vp._asdict(),
        cafile=cafile,
        capath=capath,
        truststore=bool(cafile["certs"] or capath["certs"]),
        openssl_conf=path_info(openssl_cnf),
        candidates=check_candidates(),
        openssl=dict(
            version=ssl.OPENSSL_VERSION,
            version_info=ssl.OPENSSL_VERSION_INFO,
        ),
    )


def main():
    json.dump(get_info(), sys.stdout, indent=2, sort_keys=False)


if __name__ == "__main__":
    main()
