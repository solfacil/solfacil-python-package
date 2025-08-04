from abc import ABC, abstractmethod


class CacheAdapterAbstract(ABC):
    def __init__(self, settings) -> None:
        ...
        
    def config(self):
        ...

    def connect(self) -> None:
        ...
        
    def disconnect(self) -> None:
        ...
    
    @abstractmethod
    def get_session(self):
        ...
