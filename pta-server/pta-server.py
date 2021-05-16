from socket import *
import os 
from exceptions.command_doesnt_exists import CommandDoesntExists
from exceptions.cump_not_done import CUMPNotDone
from exceptions.user_is_invalid import UserIsInvalid
from exceptions.no_given_user import NoGivenUser


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
    

    def readCommand(self, cmd, arg = None):
        if cmd == "CUMP":
            self.checkIfUserIsValid(arg)
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

                msg_terms = msg.split(' ', 2)

                # PEDIDO:
                # SEQ_NUM COMMAND ARGS_PEDIDO
                SEQ_NUM = msg_terms[0]
                COMMAND = msg_terms[1]
                ARGS_PEDIDO = None

                if len(msg_terms) == 3:
                    ARGS_PEDIDO = msg_terms[2]
                
                print(COMMAND)

                # RESPOSTA:
                # SEQ_NUM REPLY ARGS_RESP
                ARGS_RESP = ''
                REPLY = ''

                
                try:
                    self.readCommand(COMMAND, ARGS_PEDIDO)
                    

                    if not self._cump_was_done and COMMAND != "CUMP":
                        raise CUMPNotDone()
                    else:
                        self._setCUMP()

                    REPLY = "OK"

                except (CommandDoesntExists, CUMPNotDone, NoGivenUser, UserIsInvalid):
                    REPLY = "NOK"
                
                finally:
                    response = SEQ_NUM + " " + REPLY 
                    if COMMAND == "LIST" or COMMAND == "PEGA":
                        response = response + " " + ARGS_RESP
                        
                    ascii = response.encode('ascii')
                    print(ascii)
                        
                    connectionSocket.send(ascii)
                    connectionSocket.close()


            except (KeyboardInterrupt, SystemError):
                self.closeSocketConnection()
                break
    

    def sendFileNames(self):
        files = self._files
        ','.join(files)
    
    def getTotalOfFiles(self):
        return self._files.__len__
    
    def checkIfUserIsValid(self, username):
        if(username is None):
            raise NoGivenUser()

        file = open('./pta-server/users.txt', 'r')
        users = file.read().splitlines()

        print(username)
        print(users)

        if(username not in users):
            raise UserIsInvalid()
        

    def closeSocketConnection(self):
        self._serverSocket.shutdown(SHUT_RDWR)
        self._serverSocket.close()
    
    def _setCUMP(self):
        self._cump_was_done = True



if(__name__ == '__main__'):
    server = PTAServer()
    print(server.getFileList())
    print(server.port)

    server.run()