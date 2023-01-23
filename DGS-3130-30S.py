# Connect to device model DGS-3130-30S
import telnetlib
import yaml
import time
import socket


# Функция для перевода форматированной строки в байтовую
def to_bytes(line):
    return f"{line}\n".encode("utf-8")

def out_green(text):
    print("\033[32m {}" .format(text))
    print("\033[0m")

def out_red(text1):
    print("\033[31m {}" .format(text1))
    print("\033[0m")

def connect_and_set_command(device_param, command, timeout):
    ip = device_param["host"]
    name = device_param["device"]
    print(f"\nПодключаюсь к {name} {ip}")
    try:
        with  telnetlib.Telnet(ip, timeout=timeout) as telnet:
            login = ""
            login += str(telnet.read_until(b'Password:'))
            telnet.write(b'Intr1X\n')
            login += str(telnet.read_until(b'>'))
            telnet.write(b'enable\n')
            login += str(telnet.read_until(b'Password:'))
            telnet.write(b'Intr1X\n')
            login += str(telnet.read_until(b'#'))
            if "#" in login:
                print(out_green("Connect is Ok"))
            telnet.write(to_bytes(command))
            time.sleep(3)
            print(telnet.read_very_eager().decode('ascii'))
            telnet.close()
            print(f"Connect with {name} {ip} is close")
    except socket.timeout:
        print(out_red(f"Timeout при подключении к {name} {ip}"))

if __name__ == "__main__":
    with open("DGS_3130.yaml") as f:
        devices =yaml.safe_load(f)
    for device in devices:
        result = connect_and_set_command(device, "show version", timeout=5)