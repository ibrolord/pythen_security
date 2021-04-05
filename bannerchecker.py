import os, sys, socket

## NEEDS TO FIX
ip = "192.168.2.80"
port = 22
vuln_list="vuln_list.txt"

def bannergrab(ip, port):
    try:
        print("[==>] Grabbing banners")
        s = socket.socket()
        socket.setdefaulttimeout(5)

        s.connect((ip, port))

        banner = s.recv(1024)
        type(banner)
        return banner

    except Exception as e:
        print(f"ERROR checkout ---- {e}")

def vulncheck(banner, vuln_list):
    with open(vuln_list) as f:
        for line in f.readlines():
            print("line " + line.strip())
            print("banner" )
            if line.strip('\n') in banner.strip('\n'):
                #print(f"{line.strip()} is in the file")
                #print("Server is Vuln: " + banner.strip('\n'))
                print("STuff")

# def file_access():
#     if  len(sys.argv) == 2:
#         filename = sys.argv[1]

#         if not os.path.isfile(filename):
#             print(f"{filename} is not in the path ")
#             exit(0)

#             if not os.access(filename, os.R_OK):
#                 print(f"{filename} access is denied")
#                 exit(0)

#         else:
#             print(f"{filename} looks good")

# def main():
#     file_access()
#     portlist = [22]
#     #for suf in range(80):
#     suf="80"
#     ip = f'192.168.2.{suf}'
#     print(ip)
#     for port in portlist:
#         print(f"{ip} {port}")
#         bannergrab(ip, port)
#         if banner:
#             print(f"[+] {ip}: {banner}")
#             vulncheck(banner, vuln_list)

# main()

def main():
    banner = bannergrab(ip, port)
    vulncheck(banner, vuln_list)
    

main()