import socket

target_host = "0.0.0.0"
target_cmdport = 7777
target_dataport = 7771
try:
    #create a client socket
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #connect the client socket to server
    client.connect((target_host,target_cmdport))

except:
    print('Can\'t connect to server.')

print('\n>Welcome to simple File server')
print('>Enter exit to exit.')
print('>Use GET [Filename] to retrieve file.')

while True:
    cmd = input('>')
    if cmd == 'exit':
        client.send(b'close')
        client.close()
        print('>See you~')
        break

    #send command
    client.send(cmd.encode('utf-8'))

    #catch response
    response = client.recv(1024).decode()
    print ('>',response)
    if response == 'FileFound!':
        try:
            f = open('/Users/Jackson/Desktop/'+cmd[4:],'wb+')
            datatunnel = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            datatunnel.connect((target_host,target_dataport))
            print ('>Connect to datatunnel')
            print ('>Receiving...')
            l = datatunnel.recv(1024)
            while (l):
                print('>Recieve packet')
                f.write(l)
                l = datatunnel.recv(1024)
            f.close()
            print('>Recieve complete')
            print('>Closing datatunnel')
        except:
            client.send(b'close')
            client.close()
            print('Error occur break.')
            break
