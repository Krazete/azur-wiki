from PIL import Image
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-i', '--input', help='file name')
args = parser.parse_args()

Image.open(args.input).convert('RGB').save('.'.join([
    *(args.input.split('.')[:-1]),
    'jpg'
]))
