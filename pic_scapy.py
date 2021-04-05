import re, zlib, cv2
from scapy.all import *

# Needs fixing

pic_dir = "pictures"
face_dir = "faces"
pcap_file = "testpcap.pcap"

def http_assembler(pcap_file):

    carved_images = 0
    faces_detected = 0

    a = rdpcap(pcap_file)

    sessions = a.sessions()

    for session in sessions:

        http_payload = ""

        for packet in sessions[session]:

            try:
                if packet[TCP].dport == 80 or packet[TCP].sport == 80:

                    # reassemble the stream
                    http_payload += str(packet[TCP].payload)

            except:
                pass

        headers = get_http_headers(http_payload)

        if headers is None:
            continue

        image, image_type = extract_image(headers,http_payload)

        if image is not None and image_type is not None:

            # store the image
            file_name = f"{pcap_file}-pic_carver_{carved_images}{image_type}"
            fd = open((f"{pictures_directory}{file_name}"), "wb")
            fd.write(image)
            fd.close()

            carved_images += 1

            # attempt face detection
            try:
                result = face_detect((f"{pictures_directory}{file_name}"), file_name)

                if result is True:
                    faces_detected += 1
            
            except:
                pass

    
    return carved_images, faces_detected

carved_images, faces_detected = http_assembler(pcap_file)

print(f"Extracted: {carved_images} images")
print(f"Detected: {faces_detected} faces")

def get_http_headers(http_payload):

    try:
        # split the headers off it its is HTTP traffic
        headers_raw = http_payload[:http_payload.index("\r\n\r\n")+2]

        # break out the headers
        headers = dict(re.findall(r"(?P<name>.*?): (?P<value>.*?)\r\n",headers_raw))

    except:
        return None

    if "Content-Type" not in headers:
        return None

    return headers

def extract_image(headers,http_payload):

    image = None
    image_type = None

    try:
        if "image" in headers['Content-Type']:

            # grab the image type and image body
            image_type = headers['Content-Type'].split("/")[1]

            image = http_payload[http_payload.index("\r\n\r\n")+4:]

            # if we detetc compression decompress the image

            try:
                if "Content-Encoding" in headers.keys():
                    if headers['Content-Encoding'] == "gzip":
                        image = zlib.decompress(image, 16+zlib.MAX_WBITS)
                    elif headers['Content-Encoding'] == "deflate":
                        image = zlib.decompress(image)

            except:
                pass

    except:
        return None,None

    return image,image_type

def face_detect(path,file_name):
    img = cv2.impread(path)
    cascade = cv2.CascadeClassifier("haarascade_frontalface_alt.xml")
    rects = cascade.detectMultiScale(img, 1.3, 4, cv2.cv.CV_HAAR_SCALE_IMAGE, (20,20))

    if len(rects) == 0:
        return False

    rects[:, 2:] += rects[:, :2]

    for x1,y1,x2,y2 in rects:
        cv2.rectangle(img,(x1,y1),(x2,y2),(127,255,0),2)

    cv2.imwrite((f"{faces_directory}/{pcap_file}-{file_name}"),img)
    return True