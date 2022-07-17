from sqlalchemy import create_engine

class SqlServer():
    def __init__(self, con_str):
        self.con_str = con_str

    def connection(self):
        return create_engine()

