import os
import re
import socket
from threading import Thread


class ClientListener(Thread):
    def __init__(self, sock: socket.socket):
        super().__init__(daemon=True)
        self.sock = sock

    def _close(self):
        self.sock.close()

    def run(self):
        filename = self.sock.recv(1024).decode()
        self.sock.sendall(b'ok')

        data = b''
        while True:
            chunk = self.sock.recv(1024)
            if chunk:
                data += chunk
            else:
                self._close()
                break
        
        if os.path.exists(filename):
            name, extension = filename.split('.')
            name += '_copy'
            copies = list(filter(lambda f: re.search(name, f), os.listdir('.')))
            if len(copies) != 0:
                print(list(map(lambda f: int(re.search('_copy(.+?).', f).group(1)), copies)))
                max_copy = max([1, 1])
                name += str(max_copy+1)

            filename = name + '.' + extension
        with open(filename, 'wb') as f:
            f.write(data)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 8800))
    sock.listen()

    while True:
        con, addr = sock.accept()
        ClientListener(con).start()


if __name__ == "__main__":
    main()