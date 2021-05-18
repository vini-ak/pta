from socket import *
import os 
from exceptions.command_doesnt_exists import CommandDoesntExists
from exceptions.cump_not_done import CUMPNotDone
from exceptions.cump_was_done import TryingToCUMPAgain
from exceptions.file_doesnt_exist import FileDoesntExist
from exceptions.user_is_invalid import UserIsInvalid
from exceptions.no_given_user import NoGivenUser
from modules.file_reader import FileReader


class PTAServer:
    def __init__(self):
        self._PORT = 11500
        self._files = self.getFileList()
        self._cump_was_done = False
        self.initializeSocket()

        self.__SEQ_NUM = None
        self.__COMMAND = None
        self.__ARGS_PEDIDO = None
        self.__REPLY = None
        self.__ARGS_RESP = None

        self._socketIsClosed = True
        

    @property
    def port(self):
        return self._PORT
    
    def initializeSocket(self):
        self._serverSocket = socket(AF_INET, SOCK_STREAM)
        self._serverSocket.bind(('', self._PORT))
        self._serverSocket.listen(1)

    
    def getFileList(self):
        return os.listdir('./pta-server/files')
    

    def readCommand(self):
        cmd = self.__COMMAND
        args = self.__ARGS_PEDIDO

        if cmd == "CUMP":
            self.checkIfUserIsValid(args)

            # Caso o usuário seja válido, ele assumirá esse valor
            # Se não, cairá em uma das exceções tratadas e receberá NOK
            self.__REPLY = "OK"

        elif cmd == "LIST":

            totalOfFiles = self.getTotalOfFiles()
            fileNames = self.sendFileNames()
            
            self.__ARGS_RESP = str(totalOfFiles) + " " + fileNames
            self.__REPLY = "ARQS" 

        elif cmd == "PEGA":
            file = self.getFileByName()

            fileSize = file.size
            fileText = file.content

            self.__ARGS_RESP = str(fileSize) + " " + str(fileText)
            self.__REPLY = "ARQ" 


        elif cmd == "TERM":
            self.__REPLY = "OK"

        else:
            raise CommandDoesntExists()

    
    def run(self):
        print("Servidor pronto para receber requisições. Digite Ctrl + C para encerrar..")
        while True:
            try:
                if(self._socketIsClosed):
                    connectionSocket, addr = self._serverSocket.accept()

                msg = connectionSocket.recv(1024).decode()
                msg_terms = msg.split(' ', 2)

                self.__SEQ_NUM = msg_terms[0]
                self.__COMMAND = msg_terms[1]

                if len(msg_terms) == 3:
                    self.__ARGS_PEDIDO = msg_terms[2]
                  
                try:
                    self.readCommand()
                    
                    if not self._cump_was_done and self.__COMMAND != "CUMP":
                        raise CUMPNotDone()
                    elif self._cump_was_done and self.__COMMAND == "CUMP":
                        raise TryingToCUMPAgain()
                    elif not self._cump_was_done:
                        self._setCUMP()
                    

                except (CommandDoesntExists, CUMPNotDone, NoGivenUser, UserIsInvalid, TryingToCUMPAgain, FileDoesntExist):
                    self.__REPLY = "NOK"
                
                finally:

                    response = self.__SEQ_NUM + " " + self.__REPLY 

                    if self.__COMMAND == "LIST" or self.__COMMAND == "PEGA":
                        response = response + " " + self.__ARGS_RESP
                        
                    ascii = response.encode('ascii')
                    connectionSocket.send(ascii)

                    # Para fechar a conexão, a resposta tem que ser diferente de OK e 
                    # os comandos não podem ser LIST ou PEGA
                    if self.__COMMAND == "TERM" or (self.__REPLY != "OK" and not (self.__COMMAND == "LIST" or (self.__COMMAND == "PEGA"))):
                        connectionSocket.close()
                        self._socketIsClosed = True

                    else:
                        self._socketIsClosed = False


            except (KeyboardInterrupt, SystemError):
                self.closeSocketConnection()
                break
    

    def sendFileNames(self):
        files = self._files
        return ','.join(files)
    
    def getTotalOfFiles(self):
        return len(self._files)
    
    def checkIfUserIsValid(self, username):
        if(username is None):
            raise NoGivenUser()

        file = open('./pta-server/users.txt', 'r')
        users = file.read().splitlines()
        
        if(username not in users):
            raise UserIsInvalid()
        

    def closeSocketConnection(self):
        self._serverSocket.shutdown(SHUT_RDWR)
        self._serverSocket.close()
    
    def _setCUMP(self):
        self._cump_was_done = True
    
    def getFileByName(self):
        fileName = self.__ARGS_PEDIDO

        if fileName not in self._files:
            raise FileDoesntExist()
        else:
            file = FileReader(fileName)
            return file
            




if(__name__ == '__main__'):
    server = PTAServer()
    server.run()