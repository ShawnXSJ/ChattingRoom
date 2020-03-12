import socket
import threading
import sys

def recv(sock, addr, name):
    Login = name + ':' + "LoginSuccess"
    sock.sendto(Login.encode('utf-8'), addr)
    while True:
        try:
            data = sock.recv(1024)
            print(data.decode('utf-8'))
        except:
            print("-----------------服务器已关闭------------------")
            exit()

def send(sock, addr, name):
    while True:
        string = input()
        message = name + ':' + string
        data = message.encode('utf-8')
        sock.sendto(data, addr)
        if string == 'EXIT':
            print("--------------连接关闭，您已退出---------------")
            sys.exit()

def main():
    ip_address = input('请输入IP地址: ')
    port = input('请输入端口号: ')
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = (ip_address, int(port))

    print("-----欢迎来到聊天室,退出聊天室请输入'EXIT'-----")

    #检查是否用户名重名
    while True:
        name = input('请输入你的名称: ')
        message = name + ':' + "LOGIN"
        s.sendto(message.encode(), server)
        data, addr = s.recvfrom(1024)
        if data.decode() == 'OK':
            print('您已经进入聊天室...')
            break
        else:   #不允许登录
            print(data.decode())    #打印不允许登录的原因

    print('----------------- %s ------------------' % name)

    #开启多线程
    tr = threading.Thread(target=recv, args=(s, server, name), daemon=True)
    ts = threading.Thread(target=send, args=(s, server, name))
    tr.start()
    ts.start()
    ts.join()
    s.close()

if __name__ == '__main__':
    main()
