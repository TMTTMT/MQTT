# import
from posixpath import basename
from tkinter import *
from PIL import Image, ImageTk
import io
import time
from urllib.request import urlopen

window = Tk()
window.title("MQTT-image")
srceenHeight = window.winfo_screenheight()
srceenWidth = window.winfo_screenwidth()
window.geometry(str(srceenWidth) + "x" + str(srceenHeight))

buffer = io.BytesIO()
image_url = "https://images.ctfassets.net/hrltx12pl8hq/7yQR5uJhwEkRfjwMFJ7bUK/dc52a0913e8ff8b5c276177890eb0129/offset_comp_772626-opt.jpg?fit=fill&w=800&h=300"
image_byt = urlopen(image_url).read()
img = Image.open(io.BytesIO(image_byt))
photo = ImageTk.PhotoImage(img)

# create a white canvas
outercanvas = Canvas(bg='white')
outercanvas.pack(side='top', fill='both', expand='yes')

innercanvas = Canvas(outercanvas, width=srceenWidth/2, height=srceenHeight*2/3)
# innercanvas.create_oval(srceenWidth/4 - 10, srceenHeight/4 - 10, srceenWidth/4 + 10, srceenHeight/4 + 10)

outercanvas.create_window(srceenWidth/2, srceenHeight/2, window=innercanvas)

# put the image on the canvas with
# create_image(xpos, ypos, image, anchor)
image_container = innercanvas.create_image(innercanvas.winfo_reqwidth(
)/2, innercanvas.winfo_reqheight()/2, image=photo)


while 1:
    window.update()

    time.sleep(5)
    image_url = "https://vodongho.com/wp-content/uploads/2022/01/android-flip-image-hero.png"

    image_byt = urlopen(image_url).read()
    img = Image.open(io.BytesIO(image_byt))
    photo2 = ImageTk.PhotoImage(img)

    innercanvas.itemconfig(image_container, image=photo2)
