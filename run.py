from os import path
from PIL import Image
import numpy

src = Image.open('test/fixtures/cat.jpg')
print(src.format, src.size, src.mode)

src = src.convert('L') # monochrome
dest = Image.new('L', src.size, color=0)

OUTPUT_DIR = 'tmp/'

# TODO: determine tile size that works based on srcage size
TILE_WIDTH = 6
TILE_HEIGHT = 12
BACKGROUND_COLOR = 190
FILL_COLOR = 255

n = 1
for x in range(0, src.size[0], TILE_WIDTH):
    for y in range(0, src.size[1], TILE_HEIGHT):
        bounds = x, y, x + TILE_WIDTH, y + TILE_HEIGHT
        tile = src.crop(bounds)

        # fill the destination tile with BACKGROUND_COLOR
        avgtile = Image.new('L', tile.size)
        data = numpy.full((TILE_WIDTH, TILE_HEIGHT), BACKGROUND_COLOR)

        # fill a portion of the height of the tile with FILL_COLOR
        # based on the average value of the source tile
        avg = int(numpy.average(tile.getdata()))
        height = int(TILE_HEIGHT * (avg / 255))
        data[0:height-1] = FILL_COLOR
        avgtile.putdata(data.flatten())

        dest.paste(avgtile, bounds)
        print('Filled tile %d to height %d' % (n, height))

        n = n + 1

filename = path.join(OUTPUT_DIR, 'averaged-cat.jpg')
dest.save(filename)
