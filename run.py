from PIL import Image
im = Image.open('test/fixtures/cat.jpg')
print(im.format, im.size, im.mode)
