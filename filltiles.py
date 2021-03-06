from argparse import ArgumentParser
from os import path
from PIL import Image
import numpy

parser = ArgumentParser(description='Render an image using an interesting method.')
parser.add_argument('infile', help='Input image to process')
parser.add_argument('--tilewidth', dest='tile_width', type=int, default=6, help='Width of the processed tiles')
parser.add_argument('--tileheight', dest='tile_height', type=int, default=12, help='Height of the processed tiles')
parser.add_argument('--bgcolor', dest='background_color', type=int, default=190, help='Background color for the rendered image')
parser.add_argument('--fillcolor', dest='fill_color', type=int, default=255, help='Fill color for the rendered image')
parser.add_argument('--outputdir', dest='output_dir', default='tmp/', help='Directory in which to output the rendered imag')
parser.add_argument('-s', '--simple', dest='simple', action='store_true')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true')
args = parser.parse_args()

src = Image.open(args.infile)
if args.verbose:
    print('Input file %s: format=%s, size=%s, mode=%s' % (args.infile, src.format, src.size, src.mode))

src = src.convert('L') # monochrome
dest = Image.new('L', src.size, color=0)

n = 1
for x in range(0, src.size[0], args.tile_width):
    for y in range(0, src.size[1], args.tile_height):
        bounds = x, y, x + args.tile_width, y + args.tile_height
        tile = src.crop(bounds)
        avg = int(numpy.average(tile.getdata()))

        if args.simple:
            avgtile = Image.new('L', tile.size, color=avg)
            if args.verbose:
                print('Filled tile %d with avg value %d' % (n, avg))
        else:
            # fill the destination tile with BACKGROUND_COLOR
            data = numpy.full((args.tile_width, args.tile_height), args.background_color)
            avgtile = Image.new('L', tile.size)

            # fill a portion of the height of the tile with FILL_COLOR
            # based on the average value of the source tile
            height = args.tile_height - int(args.tile_height * (avg / 255))
            data[0:height-1] = args.fill_color
            avgtile.putdata(data.flatten())

            if args.verbose:
                print('Filled tile %d to height %d for avg value %d' % (n, height, avg))

        dest.paste(avgtile, bounds)


        n = n + 1

filename = path.join(args.output_dir, 'output.jpg')
dest.save(filename)
print('Saved output file to %s' % filename)
