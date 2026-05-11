import socket
import threading
from datetime import datetime

print("=" * 60)
print(" TELECOM NETWORK RECON TOOL ")
print("=" * 60)

target = input("Enter target IP or hostname: ")

try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("Invalid hostname.")
    exit()

print(f"\nScanning Target: {target_ip}")
print(f"Time Started: {datetime.now()}")
print("-" * 60)

ports = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 445, 3306, 8080]

lock = threading.Lock()

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No banner detected"

            with lock:
                print(f"[OPEN] Port {port}")
                print(f"       Service Banner: {banner}")

        sock.close()

    except:
        pass

threads = []

for port in ports:
    thread = threading.Thread(target=scan_port, args=(port,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

print("\nScan Completed.")
