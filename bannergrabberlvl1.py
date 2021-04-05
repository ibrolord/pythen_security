import socket, sys

def grabbanner(ip, port):
    try:
        socket.setdefaulttimeout(2)
        s = socket.socket()
        s.connect((ip, port))
        banner = s.recv(1024)
        return banner
    except:
        return

def main():
    ip1 = sys.argv[1]
    ip2 = sys.argv[2]
    port = sys.argv[3]
    banner1 = grabbanner(ip1, port)
    if banner1:
        print(f"[+] ip1: {banner1}")
    banner2 = grabbanner(ip2, port)
    if banner2:
        print(f"[+] ip2: {banner2}")

main()