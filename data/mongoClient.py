import pymango
import gridfs
from data import logger

class Client(object):

    def __init__(self, server: str):

        self.__server = server

    @property
    def server(self) -> str:
        return self.__server

    @property
    def short_term_memory(self) -> list:
        return self.__short_term_memory 

    def connect(self, db: str, collection: str = None, grid: bool = False) -> None:

        self.client = pymongo.MongoClient(self.server)
        logger.info(f'Client Connected to server: {self.server}')

        if grid:
            self.database = gridfs.GridFS(db)
            msg = f'Client Connected to database: {db} with Grid File System'
        else:
            self.database = self.client[f'{db}']
            self.collection = self.database[f'{collection}']
            msg = f'Client Connected to database: {db} | Collection: {collection}'

        logger.info(msg)

    def _gridPut(self, data: bytes, filename: str) -> None:

        _id = self.database.put(data, filename=filename)

        return _id

    def _gridGet(self, gridId: dict) -> bytes:
        return self.database.get(gridId)

    def _get_last(self, filename: str) -> dict:
        return {
            'data': self.database.get_last_version(filename=filename)
        }

    def _chronological(self, limit: int = 5) -> list:
        return self.database.find().sort("uploadDate", -1).limit(limit)

    def _checkFile(self, filename: str) -> bool:
       return self.database.exists({
                'filename':filename
            })

    