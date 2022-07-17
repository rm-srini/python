from abc import ABC, abstractmethod

class Database(ABC):
    def __int__(self, db_source):
        self.db_source = db_source

    @abstractmethod
    def get_connection_str(self):
        self.db_source


