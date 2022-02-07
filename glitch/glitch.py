import io
import os
import copy
import random
from PIL import Image
import logging


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


