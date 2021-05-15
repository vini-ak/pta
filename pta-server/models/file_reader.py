import os

class FileReader:
    def __init__(self, name) -> None:
        self._name = name
        self._size = self._setFileSize()
    
    @property
    def fileName(self):
        return self._name
    
    @property
    def fileSize(self):
        return self._size
    
    
    def _setFileSize(self):
        os.path.getsize(self._name)
    
    # def _setFileContent(self):
        
