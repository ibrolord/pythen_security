import sys, socket, getopt, threading, subprocess

listen = False
command = False
upload = False
execute = ""
target = ""
upload_destination = ""
port = 0


def client_sender(buffer):

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect
        client.connect((target,port))

        if len(buffer):
            client.send(buffer)            

        while True:

            # getting data back
            recv_len = 1
            response = ""

            while recv_len:

                data = client.recv(4096)
                recv_len = len(data)
                response += data

                if recv_len < 4096:
                    break

            print response,

            # wait for more input
            buffer = raw_input("")
            buffer += "\n"

            # send it off
            client.send(buffer)

    except:
        print "[*] Exception! Canceling."

        # tear down connection
        client.close()


def server_loop():
    global target

    # Listen on all target if none is defined
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        # spin off a thread to handle client
        client_thread =  threading.Thread(target=client_handler, args=(client_socket,))
        client_thread.start()    

def run_command(command):

    # trim newline
    command = command.rstrip()

    # run the command
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell=True)

    except:
        output = "Failed to execute command.\r\n"

    # send the output to the client
    return output


def client_handler(client_socket):
    global upload
    global execute
    global command

    # check for upload
    if len(upload_destination):

        # read in all bytes and write to dest
        file_buffer = ""

        # keep reading data
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        try:
            file_descriptor = open(upload_destination,"wb")
            file_descriptor.write(file_buffer)
            file_descriptor.close()

            client_socket.send("Successfully saved file to %s\r\n" % upload_destination)
        except:
            client_socket.send("Failed to save file to %s\r\n" % upload_destination)

    # check for command exec
    if len(execute):
        # run the cmd
        output = run_command(execute)

        client_socket.send(output)

    if command:

        while True:
            client_socket.send("<Poormannetcat:#> ")

            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            # send back the cmd output
            response = run_command(cmd_buffer)

            # send cack the response
            client_socket.send(response)


def usage():
    print "Ibro Net Tool --  Poorman's NetCat"
    print
    print "Usage: poormannetcat.py -t target_host -p port"
    print "-l --listen              - listen on [host]:[port] for incoming connections"
    print "-e --execute=file_to_run - execute the given file upon receiving a connection"
    print "-c --command             - initialize a command shell"
    print "-u --upload=destination  - upon receiving connection upload a file and write to [destination]"
    print
    print
    print "Examples: "
    print "poormannetcat.py -t 10.0.0.2 -p 6969 -l -c"
    print "poormannetcat.py -t 10.0.0.2 -p 6969 -l -u=/tmp/xxx.txt"
    print "poormannetcat.py -t 10.0.0.2 -p 6969 -l -e=/tmp/xxx.txt"
    print "echo 'RANDOM_TEXTS' | ./poormannetcat.py -t 10.4.2.1 -p 420"
    sys.exit(0)

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target

    if not len(sys.argv[1:]):
        usage()

    # See cmdline optns
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hle:t:p:cu:", ["help", "listen","execute","target","port","command","upload"])
    
    except getopt.GetoptError as err:
        print str(err)
        usage()

    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u", "--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)
        else:
            assert False,"Unhandled Option"


    if not listen and len(target) and port > 0:
        # read the buffer from cmdline
        buffer = sys.stdin.read()

        # send data off
        client_sender(buffer)


    if listen:
        server_loop()

main() 

