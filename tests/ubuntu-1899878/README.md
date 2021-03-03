# Reproducer for test_ssl failures and internal error in handshake

* https://bugs.launchpad.net/ubuntu/+source/openssl/+bug/1899878
* https://bugs.python.org/issue43382
* https://bugs.python.org/issue41561

```
Traceback (most recent call last):
  File "/internalerror.py", line 15, in <module>
    s.connect((HOST, server.port))
  File "/usr/lib/python3.8/ssl.py", line 1342, in connect
    self._real_connect(addr, False)
  File "/usr/lib/python3.8/ssl.py", line 1333, in _real_connect
    self.do_handshake()
  File "/usr/lib/python3.8/ssl.py", line 1309, in do_handshake
    self._sslobj.do_handshake()
ssl.SSLError: [SSL: TLSV1_ALERT_INTERNAL_ERROR] tlsv1 alert internal error (_ssl.c:1123)
```
