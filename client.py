import sys
import socket


def main():
    assert len(sys.argv)==4, f'Got {len(sys.argv)-1} arguments, 3 needed'
    _, file, ip, port = sys.argv

    with open(file, 'rb') as f:
        data = f.read()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, int(port)))

    sock.sendall(file.encode())
    sock.recv(2)
    
    sended = 0
    file_size = len(data)
    while len(data) > 0:
        sent = sock.send(data)
        sended += sent
        data = data[sent:]
        print(f'\rProgress: {int(sended/file_size*100)}%', end='')
    print(f'\rProgress: 100%')

if __name__ == "__main__":
    main()
