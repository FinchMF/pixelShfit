import sys
import logging

logging.basicConfig(
    format='%(asctime)s [%(levelname)s] %(name)s - [ %(filename)s: %(lineno)d @ %(funcName)s ] - %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    stream=sys.stdout,
)
logger = logging.getLogger('Glitcher')