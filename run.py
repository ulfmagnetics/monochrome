from os import path
from PIL import Image

im = Image.open('test/fixtures/cat.jpg')
print(im.format, im.size, im.mode)

# TODO: convert the image to a single color channel

# TODO: determine tile size that works based on image size
TILE_WIDTH = 100
TILE_HEIGHT = 100
TILE_DIR = 'tmp/'

n = 1
for x in range(0, im.size[0], TILE_WIDTH):
    for y in range(0, im.size[1], TILE_HEIGHT):
        bounds = x, y, x + TILE_WIDTH, y + TILE_HEIGHT
        tile = im.crop(bounds)

        # TODO: calculate a single value to represent how much of the single color is in this tile

        filename = path.join(TILE_DIR, 'tile%d.jpg' % n)
        tile.save(filename)
        n = n + 1
