from dxhidlib import fingerprint

if __name__ == '__main__':
    ip, mac, device = fingerprint('192.168.0.14', 'discover')
    print("IP: " + ip)
    print("MAC: " + mac)
    print("Device: " + device)
    

