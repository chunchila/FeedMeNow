import socket
import threading

if __name__ == "__main__":

    print("this is sparta")
    for x in range(100):
        print(x)
    tName = threading.current_thread().getName()

    print("im in thread ", tName)

    serverAddress = ("localhost", 80)
    sock = socket.socket()
    sock.bind(serverAddress)

    while True:
        con, client = sock.accept()

        print("got con from ", )
