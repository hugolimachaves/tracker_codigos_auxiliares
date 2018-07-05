from PIL import Image

img = Image.open('img.jpg')
img2 = img.crop((0,0,100,100))
img2.save('img2.jpg')