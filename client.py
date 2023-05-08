# SMART DEVICE

import socket
import time
import random
from concurrent.futures import ThreadPoolExecutor

DEFAULT_BUFLEN = 1400
PORT_NUM = 1337
BROADCAST_IP = "192.168.0.255"

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind the socket to the address and port
sock.bind((BROADCAST_IP, PORT_NUM))

# Set socket options to allow broadcast
sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Generate NOTIFY SSDP message
def gen_notify_ssdp(isAlive):
    nts_value = "alive" if isAlive else "byebye"
    return f'NOTIFY * HTTP/1.1\r\nHOST: 192.168.0.255:1337\r\nCACHE-CONTROL: max-age=99999\r\nLOCATION: null\r\nNT: notify\r\nNTS: ssdp:{nts_value}\r\nSERVER: Raspbian GNU/Linux 10\r\nUSN: 1\r\nBOOTID.UPNP.ORG: null.\r\nCONFIGID.UPNP.ORG: a51d4fae-7dec-11d0-a765-00a0c91e6bf6.\r\nSEARCHPORT.UPNP.ORG: null'

# Handle NOTIFY response
def handle_notify_ssdp(dst_ip, max_delay):
    delay = random.uniform(0, max_delay)
    time.sleep(delay)
    response = gen_notify_ssdp(True)
    dst_address = (dst_ip, PORT_NUM)
    sock.sendto(response.encode("utf-8"), dst_address)
    print(f"\n[!] NOTIFY sent to {dst_address} with delay {delay:.2f}s, MX was {max_delay}s\n")


# Listen for broadcasted UDP datagrams
with ThreadPoolExecutor(max_workers=5) as executor:
    print("\nListening for M-SEARCH requests...\n")
    while True:
        data, addr = sock.recvfrom(DEFAULT_BUFLEN)
        message = data.decode("utf-8")
        if message.startswith("M-SEARCH"):
            # Extract values from M_SEARCH request
            message_lines = message.splitlines()
            MX = float(message_lines[3].split(" ")[1])
            USER_AGENT = message_lines[5].split(" ")[1]

            print("\nReceived packet from:", addr[0], USER_AGENT)
            print(f"Packet contents:\n{message}\n")
            executor.submit(handle_notify_ssdp, addr[0], MX)
        else:
            print("\n[!] Got something else else\n")
