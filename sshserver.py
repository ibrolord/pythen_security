import paramiko, threading, sys, socket

host_key = paramiko.RSAKey(filename='test_rsa.key')

class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind, chanid):
        if kind == 'session':
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED
    def check_auth_password(self, username, password):
        if (username == 'ibro') and (password == '8tnLfx1J270lg'):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

server = sys.argv[1]

ssh_port = int(sys.argv[2])

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((server, ssh_port))
    sock.listen(100)
    print("[+] Listening for connection ...")
    client, addr = sock.accept()

except Exception as e:
    print('[-] Listen failed: ' + str(e))
    sys.exit(1)

print ('[+] COnnection happened')

try:
    ibroSession = paramiko.Transport(client)
    ibroSession.add_server_key(host_key)
    server = Server()

    try:
        ibroSession.start_server(server=server)
    except paramiko.SSHException as x:
        print('[-] SSH negotiation failed')
    chan = ibroSession.accept(20)
    print('[+] Authenticated!')
    print(chan.recv(1024))
    chan.send('Welcome to ibro_ssh')
    while True:
        try:
            command = input("Enter command: ").strip('\n')
            if command != 'exit':
                chan.send(command)
                print(chan.recv(1024) + '\n')
            else:
                chan.send('exit')
                print('exiting') 
                ibroSession.close()
                raise Exception ('exit')
        except KeyboardInterrupt:
            ibroSession.close()
except Exception as e:
    print('[-] Caught execption: ' + str(e))
    try:
        ibroSession.close()
    except:
        pass
    sys.exit(1)