from PIL import Image


def size(filepath):
    height = Image.open(filepath).size
    return height
