#!/usr/bin/env python3
import datetime
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

OPENSSLDIR_CANDIDATES = ("/etc/ssl", "/etc/pki/tls")
CAFILE_CANDIDATES = [
    # Taken from https://golang.org/src/crypto/x509/root_linux.go
    # and PyOpenSSL
    "/etc/ssl/certs/ca-certificates.crt",  # Debian/Ubuntu/Gentoo etc.
    "/etc/pki/tls/certs/ca-bundle.crt",  # Fedora/RHEL 6
    "/etc/ssl/ca-bundle.pem",  # OpenSUSE
    "/etc/pki/tls/cacert.pem",  # OpenELEC
    "/etc/pki/ca-trust/extracted/pem/tls-ca-bundle.pem",  # CentOS/RHEL 7
    # additional locations for RH platforms (CentOS, Fedora, RHEL)
    "/etc/ssl/certs/ca-bundle.crt",
    "/etc/ssl/certs/ca-bundle.trust.crt",
    "/etc/pki/tls/certs/ca-bundle.trust.crt",
]


def resolve_symlink(path):
    dest = path
    while True:
        try:
            dest = os.path.abspath(os.path.join(dest, os.readlink(dest)))
        except OSError:
            break
    return dest


def path_info(path):
    if path and os.path.isfile(path):
        with open(path) as f:
            certs = _pem_re.findall(f.read())
        return dict(
            path=path,
            resolved=resolve_symlink(path),
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
            resolved=resolve_symlink(path),
            exists=True,
            type="dir",
            size=len(files),
            certs=len(certs),
        )
    return dict(
        path=path, resolved=None, exists=False, type=None, size=0, certs=0,
    )


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


def check_openssldir_candidates(candidates=OPENSSLDIR_CANDIDATES):
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


def check_cafile_candidates(candidates=CAFILE_CANDIDATES):
    return {candidate: path_info(candidate) for candidate in candidates}


def check_default_context():
    ctx = ssl.create_default_context()
    result = dict(
        ca_certs_count=len(ctx.get_ca_certs()),
        options_repr=repr(ctx.options),
        verify_flags_repr=repr(ctx.verify_flags),
    )
    if hasattr(ctx, "get_ciphers"):
        result.update(
            ciphers=[c["name"] for c in ctx.get_ciphers()],
        )
    if hasattr(ctx, "minimum_version"):
        result.update(
            minimum_version=ctx.minimum_version.name,
            maximum_version=ctx.maximum_version.name,
        )
    return result


def get_info():
    vp = ssl.get_default_verify_paths()
    openssl_cnf = os.path.join(
        os.path.dirname(vp.openssl_cafile), "openssl.cnf"
    )
    cafile = path_info(vp.cafile)
    capath = path_info(vp.capath)

    return dict(
        os_release=read_os_release(),
        sys_platform=sys.platform,
        os_name=os.name,
        timestamp=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        default_verify_paths=vp._asdict(),
        cafile=cafile,
        capath=capath,
        truststore=bool(cafile["certs"] or capath["certs"]),
        openssl_conf=path_info(openssl_cnf),
        openssldir_candidates=check_openssldir_candidates(),
        cafile_candidates=check_cafile_candidates(),
        default_context=check_default_context(),
        openssl=dict(
            version=ssl.OPENSSL_VERSION,
            version_info=ssl.OPENSSL_VERSION_INFO,
        ),
    )


def main():
    json.dump(get_info(), sys.stdout, indent=2, sort_keys=False)


if __name__ == "__main__":
    main()
