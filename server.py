import socket

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    ip_address = '127.0.0.1'
    port = input('请输入端口号: ')

    s.bind((ip_address, int(port)))
    print('UDP Server on %s:%s...' % (ip_address, port))

    userlist = {}  # {addr:name}
    while True:
        try:
            data, addr = s.recvfrom(1024)
            datalist = data.decode('utf-8').split(':')
            print(data.decode('utf-8'))
            if datalist[1] == 'LOGIN':#如果是进入聊天室请求
                if (datalist[0] in userlist.values()):
                    s.sendto('该用户已经存在！'.encode(), addr)
                else:
                    s.sendto('OK'.encode(), addr)

            # 用户成功登录
            elif datalist[1] == 'LoginSuccess':
                print("[ %s ] Enter..." % datalist[0])
                for address in userlist:
                    s.sendto(datalist[0].encode() + ' 进入聊天室...'.encode(), address)
                userlist[addr] = datalist[0]
                continue

            elif datalist[1] == 'EXIT':
                #name = userlist[addr]
                name = datalist[0]
                userlist.pop(addr)
                print("[ %s ] Leave..." % name)
                for address in userlist:
                    s.sendto((name + ' 离开了聊天室...').encode(), address)

            else:
                print('"%s" from %s:%s' %
                      (data.decode('utf-8'), addr[0], addr[1]))
                for address in userlist:
                    if address != addr:
                        s.sendto(data, address)

        except ConnectionResetError:
            print('Someone left unexcept.')

if __name__ == "__main__":
    main()
