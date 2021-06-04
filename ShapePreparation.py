from PIL import Image

img = Image.open('scratch.png')

for angle in range(360):
    # converted to have an alpha layer
    im2 = img.convert('RGBA')
    # rotated image
    rot = im2.rotate(angle, expand=1)
    # a white image same size as rotated image
    fff = Image.new('RGBA', rot.size, (255,)*4)
    # create a composite image using the alpha layer of rot as a mask
    out = Image.composite(rot, fff, rot)
    # save your work (converting back to mode='1' or whatever..)
    out.convert(img.mode).save('icons/' + str(angle) + '.gif')

img = Image.open('flag.png')
img.resize((70, 70)).save('flag.gif')
