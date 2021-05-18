import os

class FileReader:
    def __init__(self, name) -> None:
        self._name = name
        self._path = os.path.join('pta-server/files/', name)
        self._size = self._setFileSize()
        self._bin_content = self._setFileContent()
    
    @property
    def name(self):
        return self._name
    
    @property
    def size(self):
        return self._size
    
    @property
    def content(self):
        return self._bin_content
    
    
    def _setFileSize(self):
        return os.path.getsize(self._path)
    
    def _setFileContent(self):
        file = open(self._path, 'rb')
        return file.read()
        
