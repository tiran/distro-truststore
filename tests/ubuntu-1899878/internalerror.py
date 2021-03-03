import ssl
import socket
from test.test_ssl import testing_context, ThreadedEchoServer, HOST

client_context, server_context, hostname = testing_context()
# client 1.0 to 1.2, server 1.0 to 1.1
client_context.minimum_version = ssl.TLSVersion.TLSv1
client_context.maximum_version = ssl.TLSVersion.TLSv1_2
server_context.minimum_version = ssl.TLSVersion.TLSv1
server_context.maximum_version = ssl.TLSVersion.TLSv1_1

with ThreadedEchoServer(context=server_context) as server:
    with client_context.wrap_socket(socket.socket(),
                                    server_hostname=hostname) as s:
        s.connect((HOST, server.port))
        assert s.version() == 'TLSv1.1'
