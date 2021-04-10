import crypt

dictFile = "dict.txt"
passFile = "pass.txt"

def checkPass(cryptPass):
    salt = cryptPass[:2]

    with open(dictFile,'r') as dFile:
        for passes in dFile:
            word = passes.strip('\n')
            cryptD = crypt.crypt(word, salt)
            if (cryptD == cryptPass):
                print(f"[+] Found the Password: {word}")
                return

        print(f"[-] Password not found")
        return

def main():
    with open(passFile) as pFile:
        for line in pFile:
            if ":" in line:
                user = line.split(":")[0]
                cryptPass = line.split(":")[1].strip(' ')
                print(f"[*] Cracking Password For: {user}")
                checkPass(cryptPass)

main()