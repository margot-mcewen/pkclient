import socket
from rich import print
import time

# run `pktriggercord-cli --servermode`
# make sure you are using a nerdfont for icons

# camera icon - \uf030
# cable icon - \U000f1394
# shutter icon - \U000f0104
# focus (flower) icon - \U000f09f1
# image icon - \U000f02e9
# deleted image icon - \U000f082b


def main():
    print_banner()

    pentax = pkclient("127.0.0.1", 8888)

    pentax.connect_server()
    pentax.connect_camera()
    pentax.get_camera_name()
    pentax.focus()
    pentax.set_aperture(2.8)
    pentax.set_shutter_speed("1/4")
    pentax.set_iso(800)

    for n in range(3):
        pentax.delete_buffer(n)

    for _ in range(3):
        pentax.shutter()
        time.sleep(0.042)

    time.sleep(0.1)  # takes a moment for shutter to write buffer

    for n in range(3):
        pentax.get_buffer(n, f"photograph_{n}")

    pentax.stop_server()


class pkclient:
    def __init__(self, host, port):
        self.sock = socket.socket()
        self.host = host
        self.port = port
        self.raw_type = None
        self.shutter_count = 0

    def connect_server(self):
        try:
            self.sock.connect((self.host, self.port))
            print(
                "[green]\U000f1394 connected to pktriggercord server:",
                end=" ",
            )
            print(f"[yellow]{self.host}[/] [magenta]{self.port}[/]")
        except ConnectionRefusedError:
            print("[red]\U000f1394 connection failed,", end=" ")
            print("[red]make sure the pktriggercord server is running")
            quit()

    def check(self):
        data = self.sock.recv(1024)
        data = data.decode().rstrip()
        if data[0] == "0":
            return True

    def stop_server(self):
        self.sock.send("stopserver".encode())
        print("[red]\U000f1394 stopping pktriggercord server")

    def connect_camera(self):
        self.sock.send("connect".encode())
        if self.check():
            print("[green]\uf030 camera connected")
        else:
            print("[red]\uf030 no camera detected")
            self.stop_server()
            quit()

    def delete_buffer(self, n):
        if n > 8:
            print(f"[red]\U000f082b THERE IS NO BUFFER {n}")
        else:
            self.sock.send(f"delete_buffer {n}".encode())
            if self.check():
                print(f"[magenta]\U000f082b buffer {n} deleted")
                if self.shutter_count > 0:
                    self.shutter_count -= 1

    def get_camera_name(self):
        self.sock.send("get_camera_name".encode())
        data = self.sock.recv(1024)
        camera_name = data.decode().rstrip()[2:]
        print(f"[yellow]\uf030 camera: {camera_name}")

    def get_current_aperture(self):
        self.sock.send("get_current_aperture".encode())
        data = self.sock.recv(1024)
        current_aperture = data.decode().rstrip()[2:]
        print(f"[yellow]\U000f0104 current aperture: {current_aperture}")

    def set_aperture(self, aperture):
        self.sock.send(f"set_aperture {aperture}".encode())
        data = self.sock.recv(1024)
        err = bool(int(data.decode()[0]))
        aperture = data.decode().rstrip()[2:]
        if err:
            print("[red]\U000f0104 invalid aperture value")
        else:
            print(f"[green]\U000f0104 aperture set to: {aperture}")

    def set_shutter_speed(self, shutter_speed):
        self.sock.send(f"set_shutter_speed {shutter_speed}".encode())
        data = self.sock.recv(1024)
        err = bool(int(data.decode()[0]))
        shutter_speed = data.decode().rstrip()[2:]
        if err:
            print("[red]\U000f0104 invalid shutter speed value")
        else:
            print(f"[green]\U000f0104 shutter speed set to: {shutter_speed}")

    def set_iso(self, iso):
        self.sock.send(f"set_iso {iso}".encode())
        data = self.sock.recv(1024)
        err = bool(int(data.decode()[0]))
        iso = data.decode().rstrip()[2:]
        if err:
            print("[red]\U000f0104 invalid iso value")
        else:
            print(f"[green]\U000f0104 iso set to: {iso}")

    def focus(self):
        self.sock.send("focus".encode())
        if self.check():
            time.sleep(1)
            print("[green]\U000f09f1 camera focused")

    def shutter(self):
        if self.shutter_count > 8:
            print(
                "[red]\U000f0104 NEVER TAKE MORE THAN 9 PHOTOS WITHOUT CLEARING BUFFER"
            )
            time.sleep(5)
        else:
            self.sock.send("shutter".encode())
            if self.check():
                print("[green]\U000f0104 photo taken")
                self.shutter_count += 1

    def get_buffer(self, n, name):
        if self.raw_type is None:
            self.get_buffer_type()
        self.sock.send(f"get_buffer {n}".encode())
        data = self.sock.recv(1024)
        data = data.decode().rstrip()
        size = int(data[2:])
        count = 0
        with open(f"{name}.{self.raw_type}", "wb") as raw:
            while count < size:
                self.sock.settimeout(10)
                try:
                    data = self.sock.recv(1024)
                except TimeoutError:
                    break
                raw.write(data)
                count = int(raw.tell())
                print(
                    f"[magenta]\U000f02e9 downloading buffer {n}: {count}/{size} bytes",
                    end="\r",
                )
            print(f"[magenta]\U000f02e9 downloading buffer {n}: {count}/{size} bytes")
            print(f"[green]\U000f02e9 image written to: {name}.{self.raw_type}")

    def set_buffer_type(self, buffer_type):
        buffer_type = buffer_type.upper()
        self.sock.send(f"set_buffer_type {buffer_type}".encode())
        data = self.sock.recv(1024)
        err = bool(int(data.decode()[0]))
        buffer_type = data.decode().rstrip()[2:]
        if err:
            print("[red]\U000f02e9 invalid raw type")
            self.get_buffer_type()
        else:
            self.raw_type = buffer_type
            print(f"[green]\U000f02e9 raw type set to: {self.raw_type}")

    def get_buffer_type(self):
        self.sock.send("get_buffer_type".encode())
        data = self.sock.recv(1024)
        buffer_type = data.decode().rstrip()[2:]
        print(f"[yellow]\U000f02e9 current raw type: {buffer_type}")
        self.raw_type = buffer_type.upper()


def print_banner():
    print("""[magenta]\
     _       _ _         _
 ___| |_ ___| |_|___ ___| |_
| . | '_|  _| | | -_|   |  _|
|  _|_,_|___|_|_|___|_|_|_|
|_|pktriggercord python client
""")


if __name__ == "__main__":
    main()
