import io
import os
import copy
import random
from PIL import Image
from glitch import logger


class BadImageException(Exception):
    pass


class Glitch(object):

    def __init__(
        self,
        pathIn: str,
        pathOut: str,
        amnt: float = None,
        seed: float = None,
        n_iter: int = None,
        max_width: int = 900,
        max_retries: int = 3,
        verbose: bool = False
    ):

        self.__pathIn: str = pathIn
        self.__pathOut: str = pathOut
        self.__amnt: float = amnt
        self.__seed: float = seed
        self.__n_iter: int = n_iter
        self.__max_width: int = max_width
        self._retries: int = max_retires
        self.__verbose: bool = verbose

    @property
    def pathIn(self) -> str:
        return self.__pathIn

    @property
    def pathOut(self) -> str:
        return self.__pathOut

    
    @property
    def amnt(self) -> float:
        return self.__amnt

    @amnt.setter
    def amnt(self, value: float):
        if isinstance(value, float):
            self.__amnt: float = value
        else:
            raise TypeError(f"Glich.amnt only supports type float\
                                | type {type(value)}  was passed")

    @property
    def seed(self) -> float:
        return self.__seed

    @seed.setter
    def seed(self, value: float):
        if isinstance(value, float):
            self.__seed: float = value
        else:
            TypeError(f'Glitch.seed only supports type float\
                        | type {type(value)} was passed')

    @property
    def n_iter(self) -> int:
        return self.__n_iter

    @n_iter.setter
    def n_iter(sefl, values: int) -> None:
        if isinstance(value, int):
            self.__n_iter: int = value
        else:
            raise TypeError(f' Glitch.n_iter only supports type int\
                               | type {type(value)} was passed')

    @property
    def max_width(self) -> int:
        return self.__max_width

    @max_width.setter
    def max_width(self, value: int) -> None:
        if isinstance(value, int):
            self.__max_width: int = value
        else:
            TypeError(f'Glitch.max_width only supporst type int\
                        | type {type(value)} was passed')

    @property
    def max_retries(self) -> int:
        return self.__max_retires

    @max_retries.setter 
    def max_retries(self, value: int) -> None:
        if isinstance(value, int):
            self.__max_retries: int = value
        else:
            raise TypeError(f'Glitch.max_retries only support int\
                            | type {type(value)} was passed')

    @property
    def verbose(self) -> bool:
        return self.__verbose 

    
    def _toBytes(self, img: object) -> None:
        """
        internal funciton to convert image signal into bytes
        """
        out: object = io.BytesIO()
        img.save(out, quality=95, format='JPEG')
        out.seek(0)
        self.data: bytes = out.read()

    def _png2data(self) -> None:
        """
        internal function to read in png image data
        """
        img: object = Image.open(self.pathIn)
        img.convert('RBG')
        self._toBytes(img=img)

    def _jpg2data(self) -> None:
        """
        internal funciton to read in jpeg image data
        """
        with open(self.pathIn, 'rb') as f:
            self.data = f.read()

    def _data2jpeg(self) -> None:
        """
        internal function to write data as jpeg image
        """
        with open(self.pathOut, 'wb') as f:
            f.write(self.dataCopy)

    def _data2png(self) -> None:
        """
        internal function to writer data as png data
        """
        try:
            stream: bytes = io.BytesIO(self.dataCopy)
            img: object = Image.open(stream)
            img.save(self.pathOut)
        
        except Exception as e:
            raise BadImageException(e)

    def readImg(self) -> None:
        """
        function to read in image data
        """
        ext: str = os.path.splitext(self.pathIn)[-1]

        if ext == '.png':
            self._png2data()

        elif ext in ('.jpg', '.jpeg', '.jpe'):
            self._jpg2data()

        else:
            raise BadImageException(f'Image extenstion {ext} is not supported.\
                                     | please use: .jpeg or .png file type')

    def writeImg(self) -> None:
        """
        function to write out image data
        """
        ext: str = os.path.splitext(self.pathOut)[-1].lower()

        if ext in ('.jpg', '.jpeg', '.jpe'):
            self._data2jpeg()

        elif ext == '.png':
            self._data2png()

        else:
            raise BadImageException(f'Image extension {ext} is not supported.\
                                    | please use: .jpeg or .png file types')

    def resize(self) -> None:
        """
        function to check and resize image
        """
        inp: object = io.BytesIO(self.data)
        img: object = Image.open(inp)

        if img.size[0] > self.max_width:

            wpercent: float = (self.max_width / float(img.size[0]))
            hsize: int = int((float(img.size[1]) * float(wpercent)))

            img: object = img.resize((self.max_width, hsize), Image.ANTIALIAS)
            self._toBytes(img=img)

    def checkVariables(self) -> None:
        """
        function to check variables and set to set random if needed
        """
        self.amnt = min(self.amnt, 1.) if self.amnt is not None else random.random()
        self.seed = min(self.seed, 1.) if self.seed is not None else random.random()
        self.n_iter = min(self.n_iter, 115) if self.n_iter else random.randint(0, 115)

    def glitch(self) -> bytes:
        """
        function to glitch image by modifying bytes

        the function returns a modified copy of the image data
        """
        found: int = self.data.find((255, 218))
        if not found: raise BadImageException('Not Valid JPEG')

        head_len: int = found + 2
        self.checkVariables()

        if self.verbose:
            logger.info(f'Data length: {len(self.data)}')
            logger.info(f'Amount: {self.amnt} | Seed: {self.seed} | n_iter: {self.n_iter}')

        max_idx: int = len(self.data) - header_len - 4
        windowSz: int = int(max_idx // self.n_iter)
        dataCopy: bytearray = bytearray(copy.copy(self.data))


        for i in range(header_len, max_idx, windowSz):

            modified_idx: int = i + int(windowSz * self.seed)
            modified_idx: int = min(modified_idx, max_idx)
            dataCopy[modified_idx]: int = int(self.amnt * 256 / 100)

        return dataCopy



        


