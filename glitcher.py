import os 
import random 
from glob import glob
from glitch.glitch import Glitch

class Glitcher(Glitch):

    """
    object to randomize parameters and automate glitch
    on a random image from a given directory
    """
    def __init__(self, image_directory: str):
        # note to self - method of connecting to images may be updated with mongoDB (gridFs)
        self.__image_directory: str = image_directory
        self.__parameters: dict = {
            'pathIn': None,
            'pathOut': None,
            'amnt': None,
            'n_iter': None,
            'verbose': None
        }
        self.initRandomizeParameters()

    @property
    def image_directory(self) -> str:
        return self.__image_directory

    @property
    def parameters(self) -> dict:
        return self.__parameters 

    def initRandomizeParameters(self) -> None:
        """
        function to generate random parameters for glitch object
        """
        images: list = glob(self.image_directory)
        rand_img_idx: int = random.randint(0, len(images)-1)

        self.parameters['pathIn']: str = images[rand_img_idx]
        self.parameters['pathOut']: str = f"./processed/glitched_{rand_img_idx}.jpg"
        self.parameters['amnt']: float = random.random()
        self.parameters['seed']: float = random.random() 
        self.parameters['n_iter']: int = random.randint(0, 60)
        super().__init__(**self.parameters)


if __name__ == '__main__':

    directory = '/Users/finchmf/Desktop/NOW/CLARITY_frames/*'
    G = Glitcher(image_directory=directory)
    G.processGlitch()