import urllib.request
from PIL import Image

def ParserImg(uri: str,n: str):
 urllib.request.urlretrieve(uri,n)
 img = Image.open(n)
 img_resize = img.resize((360, 168))
 img_resize.save(n,quality=100)
