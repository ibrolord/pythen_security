import nmap, argparse, sys

# pip3 install python-nmap

def nmapScan(tgtHost, tgtPorts):
    nmScan = nmap.PortScanner()
    for tgtPort in tgtPorts:
        nmScan.scan(tgtHost, tgtPort)
        state = nmScan[tgtHost]['tcp'][int(tgtPort)]['state']
        
        print(f"[*] {tgtHost} tcp/{tgtPort} {state}")

def main():
    parser = argparse.ArgumentParser(usage=f'usage {sys.argv[0]} -H <target host> -p <target port> \nexample: python3 {sys.argv[0]} -H 10.0.0.69 -p 69,96')

    parser.add_argument('-H', required=True, dest='tgtHost', type=str, help='Specify target Host')
    parser.add_argument('-p', required=True, dest='tgtPort', type=str, help='Specify target port[s] comma seprated (no space')

    args = parser.parse_args()

    tgtHost = args.tgtHost
    tgtPorts = str(args.tgtPort).split(',')

    nmapScan(tgtHost, tgtPorts)

main()