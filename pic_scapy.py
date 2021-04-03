import re, zlib, cv2
from scapy.all import *

pic_dir = "pictures"
face_dir = "faces"
pcap_file = "testpcap.pcap"

def http_assembler(pcap_file):

    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    # for session in sessions:

    #     http_payload = ""

    #     for packet in sessions[session]:

    #         try:
    #             if packet[TCP].dport == 80 or packet[TCP].sport == 80:

    #                 # reassemble the stream
    #                 http_payload += str(packet[TCP].payload)

    #         except:
    #             pass

    #     headers 

http_assembler(pcap_file)

