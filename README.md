# Practical Exam
Bibliotecas utilizadas:

- **socket**: essa lib está sendo utilizada para podermos criar uma conexão TCP/IP entre o cliente e o servidor.
- **os** esta lib é utilizada para facilitar as operações que são executadas pelo sistema operacional. Estou utilizando para pegar informações relativas aos paths de arquivos e diretórios e recuperar algumas informações sobre os arquivos (ex: tamanho do arquivo em bytes).


Organização do projeto ([pta-server/]):

- **exceptions/**: contém as exceções para os tratamentos de erro do servidor.
- **files/**: contém os arquivos a serem consultados pelo cliente com os comandos [PEGA] e [TERM].
- **modules/**: criado para modularizar e organizar o projeto em objetos menores. No caso, criei apenas o módulo [FileReader]
    -- **file_reader.py**: módulo para capturar as informações de um arquivo. Ele será usado quando o cliente enviar um comando [PEGA].
- **pta-server.py**: arquivo do servidor.
- **user.txt**: lista de usuários que possuem acesso ao PTA.
