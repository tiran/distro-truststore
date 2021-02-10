# distro-truststore
Linux distribution CA store test

Name | can verify | loaded CA certs | CA file | CA path | path certs | OpenSSL version
--- | --- | --- | --- | --- | --- | ---
alpine:latest | :heavy_check_mark: | 137 | /etc/ssl/cert.pem | /etc/ssl/certs | 0 | OpenSSL 1.1.1i  8 Dec 2020
archlinux:latest | :heavy_check_mark: | 138 | /etc/ssl/cert.pem | /etc/ssl/certs | 276 | OpenSSL 1.1.1h  22 Sep 2020
CentOS 7 | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.0.2k-fips  26 Jan 2017
CentOS 8 | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.1.1g FIPS  21 Apr 2020
Debian Buster with ca-certificates | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 137 | OpenSSL 1.1.1d  10 Sep 2019
Debian Buster | :x: | 0 |  |  | 0 | OpenSSL 1.1.1d  10 Sep 2019
Debian testing with ca-certificates | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 129 | OpenSSL 1.1.1i  8 Dec 2020
Debian testing | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 129 | OpenSSL 1.1.1i  8 Dec 2020
Fedora 32 | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.1.1i FIPS  8 Dec 2020
Fedora 33 | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.1.1i FIPS  8 Dec 2020
Fedora 34 | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.1.1i FIPS  8 Dec 2020
Fedora Rawhode | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.1.1i FIPS  8 Dec 2020
FreeBSD pkg python3 ca_root_nss | :heavy_check_mark: | 148 | /etc/ssl/cert.pem |  | 0 | OpenSSL 1.1.1d-freebsd  10 Sep 2019
FreeBSD pkg python3 | :x: | 0 |  |  | 0 | OpenSSL 1.1.1d-freebsd  10 Sep 2019
Gentoo Stage 3 latest | :heavy_check_mark: | 0 |  | /etc/ssl/certs | 126 | OpenSSL 1.1.1g  21 Apr 2020
Linux Mint 19.3 | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 129 | OpenSSL 1.1.1  11 Sep 2018
openSUSE Tumbleweed | :heavy_check_mark: | 138 | /var/lib/ca-certificates/ca-bundle.pem | /var/lib/ca-certificates/openssl | 296 | OpenSSL 1.1.1h  22 Sep 2020
OpenWRT RootFS | :heavy_check_mark: | 129 | /etc/ssl/cert.pem | /etc/ssl/certs | 0 | OpenSSL 1.1.1i  8 Dec 2020
macos-latest | :heavy_check_mark: | 164 | /usr/local/etc/openssl@1.1/cert.pem | /usr/local/etc/openssl@1.1/certs | 0 | OpenSSL 1.1.1i  8 Dec 2020
windows-latest | :heavy_check_mark: | 362 |  |  | 0 | OpenSSL 1.1.1g  21 Apr 2020
RHEL 8.3 UBI | :heavy_check_mark: | 136 | /etc/pki/tls/cert.pem | /etc/pki/tls/certs | 0 | OpenSSL 1.1.1g FIPS  21 Apr 2020
Ubuntu Bionic with ca-certificates | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 129 | OpenSSL 1.1.1  11 Sep 2018
Ubuntu Focal with ca-certificates | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 129 | OpenSSL 1.1.1f  31 Mar 2020
Ubuntu Focal with deadsnakes python3.9 | :x: | 0 |  |  | 0 | OpenSSL 1.1.1f  31 Mar 2020
Ubuntu Focal | :x: | 0 |  |  | 0 | OpenSSL 1.1.1f  31 Mar 2020
Ubuntu Groovy | :x: | 0 |  |  | 0 | OpenSSL 1.1.1f  31 Mar 2020
Ubuntu Xenial with ca-certificates | :heavy_check_mark: | 0 |  | /usr/lib/ssl/certs | 258 | OpenSSL 1.0.2g  1 Mar 2016



## issues

* [Fedora feature request](https://bugzilla.redhat.com/show_bug.cgi?id=1895619)
  to make ``/etc/ssl`` a working OpenSSL config directory with trust store.
* [Debian bug](https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=960869)
  make Python depend on ``ca-certificate``
* [Ubuntu bug](https://bugs.launchpad.net/ubuntu/+source/python3.6/+bug/1879310)
  make Python depend on ``ca-certificate``
* [Deadsnakes PPA request](https://github.com/deadsnakes/issues/issues/144)
  to make Python depend on ``ca-certificate``
