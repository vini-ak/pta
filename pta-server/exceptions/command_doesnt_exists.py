class CommandDoesntExists(Exception):
    '''
    Exceção para quando o usuário passar um comando diferente de:
        - CUMP
        - LIST
        - PEGA
        - TERM
    '''
