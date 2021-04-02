import sys, socket, threading, re

CEND = '\33[0m'
CRED2 = '\33[91m'
CRED = '\33[31m'
CGREEN = '\33[32m'
CBLINK = '\33[5m'
CBLINK2 = '\33[6m'
CBLUE = '\33[34m'




def hexdump(src, length=16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2

    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join(["%0*X" % (digits, ord(x)) for x in s])
        text = b''.join([x if 0x20 <= ord(x) < 0x7F else b'.' for x in s])
        result.append( b"%/04X %-*s %s" % (i, length*(digits + 1), hexa, text) )

    print (b'\n'.join(result))

def receive_from(connection):

    buffer = ""

    # We set a 2 second timeout 
    connection.settimeout(2)

    try:
        # keep reading into the buffer until there's no more data
        while True:
            data = connection.recv(4096)

            if not data:
                break

            buffer += data

    except:
        pass

    return buffer


def request_handler(buffer):
    # perform packet modifications
    return buffer

def response_handler(buffer):
    # perform packet modifications
    return buffer



def proxy_handler(client_socket, remote_host, remote_port, receive_first):

    # connect to the remote host
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    # receive data from the remote end if necessary
    if receive_first:

        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        # send it to our response handler
        remote_buffer = response_handler(remote_buffer)

        # send data if we have data to send to our local client
        if len(remote_buffer):
            print("[<==] Sending {} bytes to localhost".format(len(remote_buffer)))
            client_socket.send(remote_buffer)
    
    #loop and read from local
    while True:

        # read from local host
        local_buffer = receive_from(client_socket)

        if len(local_buffer):

            print("[==>] Received {} bytes from localhost.".format(len(local_buffer)))
            hexdump(local_buffer)

            # send it to request handler
            local_buffer = request_handler(local_buffer)

            # send off the data to the remote host
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

            # receive back the response
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):

                print("[<==] Received {} bytes from remote.".format(len(remote_buffer)))
                hexdump(remote_buffer)

                # send to response handler
                remote_buffer = response_handler(remote_buffer)

                # send the response to the local socket
                client_socket.send(remote_buffer)

                print("[<==] Sent to localhost.")

            # close connections if no more data
            if not len(local_buffer) or not len(remote_buffer):
                client_socket.closef()
                remote_socket.close()
                print("[*] No more data. Closing connections")

                break


def server_loop(local_host, local_port, remote_host, remote_port, reveive_first):

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host,local_port))

    except socket.error as err:
        print (CRED2 + "[!!] Failed to listen on {}:{}".format(local_host,local_port) + CEND)
        print(CRED2 + "[!!] Check for other listening sockets or correct permissions" + CEND)
        print(CRED2 + f"[!!] Caught execption error: {err}")
        sys.exit(0)

    print(CGREEN + "[*] Listening on {}.{}".format(local_host,local_port) + CEND)

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # print out the local connection info
        print (CBLUE + "[==>] Received incoming connection from {}:{}".format(addr[0],addr[1]) + CEND)

        # start a thread to talk to the remote host 
        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket,remote_host,remote_port,reveive_first))
        proxy_thread.start()



def main():

    if len(sys.argv[1:]) != 5:
        print("Usage: ./tcpproxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("Example: ./tcpproxy.py 10.4.2.1 6969 10.4.2.2 9696 True")
        sys.exit(0)

    # setup local & target listening parameters
    # if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",sys.argv[1]):
        local_host = sys.argv[1]
        local_port = int(sys.argv[2])
    # else:
    #     print("IP Format is off, what you have is {} ".format(sys.argv[1]))


    # if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",sys.argv[3]):
        remote_host = sys.argv[3]
        remote_port = int(sys.argv[4])
    # else:
    #     print("IP Format is off, what you have is {} ".format(sys.argv[3]))

        # Connect and receive data before sending to remote host
        receive_first = sys.argv[5]

        if "True" in receive_first:
            receive_first = True
        else:
            receive_first = False

        # listening socket        
        server_loop(local_host,local_port,remote_host,remote_host,receive_first)

main()

