__author__ = 'jungletech'

from PIL import Image

image = Image.open('reddit_me_irl_3fixaz_album_None_imgur_pTaGzzz.jpg')
image = image.resize((300, 300), Image.ANTIALIAS)
image.save('pizza.jpg')

