from socket import *
import os 
from enums import *
from exceptions import *

class PTAServer:
    def __init__(self):
        self._PORT = 11500
        self._files = self.getFileList()
        self._cump_was_done = False
        self.initializeSocket()
        

    @property
    def port(self):
        return self._PORT
    
    def initializeSocket(self):
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self._serverSocket.bind(('', self._PORT))
        self._serverSocket.listen(1)

    
    def getFileList(self):
        return os.listdir('./pta-server/files')
    

    def readCommand(self, cmd):
        if cmd == "CUMP":
            print()
        elif cmd == "LIST":
            print()
        elif cmd == "PEGA":
            print()
        elif cmd == "TERM":
            print()
        else:
            raise CommandDoesntExists()

    
    def run(self):
        print("Servidor pronto para receber requisições. Digite Ctrl + C para encerrar..")
        while True:
            try:
                connectionSocket, addr = self._serverSocket.accept()
                msg = connectionSocket.recv(1024).decode()
                print(msg)

                SEQ_NUM, COMMAND, ARGS_PEDIDO = msg.split(' ', 2)

                try:
                    
                    ARGS_RESP = ''
                    REPLY = ''

                    if not self._cump_was_done:
                        raise CUMPNotDone()

                    self.readCommand(COMMAND)
                    REPLY = "OK"

                except (UserIsInvalid, CUMPNotDone):
                    REPLY = "NOK"
                    self.closeSocketConnection()

                finally:
                    response = SEQ_NUM + " " + REPLY 
                    
                    + " " + ARGS_RESP
                    self._serverSocket.send(response.encode('ascii'))


            except (KeyboardInterrupt, SystemError):
                self.closeSocketConnection()
                break
    

    def sendFileNames(self):
        files = self._files
        ','.join(files)
    
    def getTotalOfFiles(self):
        return self._files.__len__
    
    def checkIfUserIsValid(self, username):
        file = open('users.txt', 'r')
        users = file.read().splitlines()

        if(username not in users):
            raise UserIsInvalid()
        

    def closeSocketConnection(self):
        self._serverSocket.shutdown(SHUT_RDWR)
        self._serverSocket.close()



if(__name__ == '__main__'):
    server = PTAServer()
    print(server.getFileList())
    print(server.port)

    server.run()