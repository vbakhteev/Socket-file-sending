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
    
    msg_size = 1024*512 # 0.5 Megabyte
    i = 0
    while i < len(data):
        chunk = data[i:max(i+msg_size, len(data))]
        sock.sendall(chunk)
        print(f'\rProgress: {int(i/len(data)*100)}%', end='')
        i += msg_size
    print(f'\rProgress: 100%')

if __name__ == "__main__":
    main()