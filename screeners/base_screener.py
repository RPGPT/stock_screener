from abc import ABC, abstractmethod

class BaseScreener(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    @abstractmethod
    def get_criteria(self) -> dict:
        pass
    
    @abstractmethod
    def get_warning_message(self) -> str:
        pass
