from configparser import ConfigParser
from data.mongoClient import Client


class ORM(Client):

    _local = ConfigParser()
    _local.read('./config')

    def __init__(self, database: str):

        super().__init__(server=ORM._local['default']['local'])
        self.__database = database
        self._short_term_memory = []

    @property
    def database(self) -> str:
        return self.__database 

    @property
    def short_term_memory(self) -> list:
        return self.__short_term_memory

    def insertImage(self, file_path: str) -> None:

        with open(file_path, 'rb') as data:
            contents = data.read()

        self.short_term_memory.append(
            self._gridPut(data=contents, filename=file_path)
        )

    def fetchImage(self, gridId: dict, file_path: str, data_out: bool) -> dict:

        bts = self._gridGet(gridId=gridId)

        with open(file_path, 'wb') as f:
            f.write(bts.read())

        if data_out:
            result = {'data': bts}

        else:
            result = {'data': None}

        return result
