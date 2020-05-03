from os import path
from PIL import Image
import numpy

src = Image.open('test/fixtures/cat.jpg')
print(src.format, src.size, src.mode)

src = src.convert('L') # monochrome
dest = Image.new('L', src.size, color=0)

# TODO: determine tile size that works based on srcage size
TILE_WIDTH = 15
TILE_HEIGHT = 15
TILE_DIR = 'tmp/'

n = 1
for x in range(0, src.size[0], TILE_WIDTH):
    for y in range(0, src.size[1], TILE_HEIGHT):
        bounds = x, y, x + TILE_WIDTH, y + TILE_HEIGHT
        tile = src.crop(bounds)

        avg = int(numpy.average(tile.getdata()))
        avgtile = Image.new('L', tile.size, color=avg)
        dest.paste(avgtile, bounds)
        print('Filled tile %d with avg value %d' % (n, avg))

        n = n + 1

filename = path.join(TILE_DIR, 'averaged-cat.jpg')
dest.save(filename)
