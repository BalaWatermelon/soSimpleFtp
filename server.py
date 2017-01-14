import os
import socket
import threading

bind_ip = "0.0.0.0"
bind_port = 7777
bind_dataport = 7771

serverFolder = os.path.dirname(os.path.abspath(__file__))
filelist = os.listdir(serverFolder)

commandList = ['get','close','h']

class cmd:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def sendfile(target,datatunnel):
    print('[*]Start sending...')
    f = open(serverFolder+'/'+target,'rb')
    packet = f.read(1024)
    while(packet):
        print('[*]Sending...')
        datatunnel.send(packet)
        packet = f.read(1024)
    f.close()
    print('[*]Send complete')
    datatunnel.close()
    print('[*]Datatunnel closed')


def handle_client(client_socket):
    while True:
        #print client recieved data
        clientmsg = client_socket.recv(1024).decode()
        request = clientmsg[0:3]
        target = clientmsg[4:]
        if request in commandList:
            if clientmsg != 'close':
                if request == 'get':
                    print ('[*] Received:',cmd.BOLD,request,cmd.ENDC,'request for',cmd.BLUE,target,cmd.ENDC)

                    #refresh filelist
                    filelist = os.listdir(serverFolder)
                    if target in filelist:
                        client_socket.send(b'FileFound!')
                        dataclient,addr = dataserver.accept()
                        dataclienthandler = threading.Thread(target=sendfile,args=(target,dataclient))
                        dataclienthandler.start()
                    else:
                        client_socket.send(b'404 not found')
                elif request == 'h':
                    client_socket.send(b'GET [filename]-retrieve file\n exit - exit program')
            else:
                print('[*]Drop client')
                client_socket.close()
                break
        else:
            client_socket.send(b'Bad request\nType help for more info.')

print('\nWelcome to pyServer.\n')
print(  '[*]Serving Folder:\n'
        ,cmd.BLUE,serverFolder,cmd.ENDC
        ,'\n\n[*]with list of files: \n'
        ,cmd.BLUE,filelist,cmd.ENDC,'\n' )

try:
    print('[*]Starting up server...')
    server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server.bind((bind_ip,bind_port))
    server.listen(5)
    dataserver = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    dataserver.bind((bind_ip,bind_dataport))
    dataserver.listen(5)
    print(cmd.GREEN,'[*]Sever started. Listening on',bind_ip,bind_port,cmd.ENDC)
    while True:

        client,addr = server.accept()

        print ("[*] Accepted connection from: %s:%d" % (addr[0],addr[1]))

        #start client process, handle recieved data
        client_handler = threading.Thread(target=handle_client,args=(client,))
        client_handler.start()
except:
    print(cmd.FAIL,'[*]Error. Server stopped.',cmd.ENDC)
