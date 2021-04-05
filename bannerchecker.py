import os, sys, socket


def file_access():
    if  len(sys.argv) == 2:
        vuln_list = sys.argv[1]

        if not os.path.isfile(vuln_list):
            print(f"{vuln_list} is not in the path ")
            exit(0)

            if not os.access(vuln_list, os.R_OK):
                print(f"{vuln_list} access is denied")
                exit(0)

        return vuln_list

    else:
        print(f"you have type an extra argument {sys.argv[2:]}, you need just 1 arg")
        exit(0)



def bannergrab(ip, port):
    try:
        print("[==>] Grabbing banners")
        s = socket.socket()
        socket.setdefaulttimeout(5)

        s.connect((ip, port))

        banner = s.recv(1024)

        return str(banner)

    except Exception as e:
        print(f"ERROR checkout ---- {e}")


def vulncheck(banner, vuln_list):
    with open(vuln_list) as f:
        for line in f.readlines():
            if line.strip('\n') in banner.strip('\n'):
                print(f"{line.strip()} is a vulnerability in the file")
                print("The exact Server Vuln: " + banner.strip('\n') + f"is gotten from {vuln_list}")


def main():

    vuln_list = file_access()

    portlist = [22]
    
    for suf in range(80,81):
        ip = f'192.168.2.{suf}'
        for port in portlist:

            print(f"Scanning ip: {ip} and port: {port}")
            banner = bannergrab(ip, port)

            if banner:
                vulncheck(banner, vuln_list)
            else:
                print(f'[-] Usage: {str(sys.argv[0])} <vuln filename>')
                exit(0)

main()